# Upstream limitation: `warn(Instance(...))` drops the warning's structured `extra`

**Status:** reported upstream, pending there. Worked around in MolSysMT.
**Upstream:** `smonitor/devguide/pending_proposals/catalog_signals_lose_structured_extra.md`
**Severity:** low here (a working pattern exists), medium upstream (it makes a rule
of the SMonitor guide unimplementable)

## What we hit

While giving `GpuNotAvailableWarning` its missing catalog template (MSM-WARN-GPU-001),
a template placeholder other than `{message}` would not interpolate:

```python
warn(GpuNotAvailableWarning(reason='the taichi package is not installed'))
# emitted: "GPU acceleration was requested but is not available: {reason} ..."
```

`{reason}` renders literally.

## Why

`smonitor.integrations.CatalogWarning.__init__` uses `extra` to resolve the message and
then discards it — only `self.message` is kept. `DiagnosticBundle.warn()` therefore
cannot recover the instance's structured data, and re-emits from the catalog with a
synthetic `extra` containing just the rendered string and the caller. Anything else the
template references stays unfilled.

The same discard happens in `CatalogException`, which is why a caught MolSysMT exception
exposes no `.code` and no `.extra` — only `catalog_key`, and that is a class attribute.

## The rule this collides with

`SMONITOR_GUIDE.md` requires:

> **Lazy Diagnostics**: Do not perform expensive string formatting before calling `emit`.
> Pass raw data in `extra` and let SMonitor handle the interpolation.

For warnings routed through `warn()`, that is currently not possible: the only way to get
a specific sentence to the user is to pre-render it and pass it as `message`, which is the
"Zero String Hardcoding" pattern the same guide forbids. That is exactly how
`GpuNotAvailableWarning` ended up carrying a hardcoded string at four call sites.

## What we do in the meantime

Emit catalog warnings as **instances through the standard warnings machinery**:

```python
import warnings
from molsysmt._private.smonitor import GpuNotAvailableWarning

warnings.warn(GpuNotAvailableWarning(reason='the taichi package is not installed'))
```

The instance hydrates its own message from the catalog correctly, so the user-facing text
is right and no string is hardcoded. This is the pattern already used by
`MemoryPressureWarning` in `_private/execution/chunked_executor.py`.

**Known cost:** this path does not go through the SMonitor emission channel, so the event
does not reach `report()`. Structured telemetry for these warnings is lost until the
upstream fix lands. That trade is deliberate: a correct user-facing message with no
telemetry beats a broken message with telemetry.

## When the upstream proposal lands

Switch these call sites back to `warn(Instance(...))` and the telemetry returns with no
change to the templates. The affected sites are `_private/gpu.py` and the taichi fallbacks
in `structure/get_angles.py`, `structure/least_rmsd_fit.py`, `structure/get_contacts.py`
and `physchem/get_sasa.py`.
