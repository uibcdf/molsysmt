# Upstream limitation: `warn(Instance(...))` drops the warning's structured `extra`

**Status:** **resolved upstream and verified on 2026-08-08.** SMonitor 0.12.0 carries
`fix(integrations): retain structured extra on catalog signals`, and is published on the
`uibcdf` conda channel.
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


## Verification, 2026-08-08

Against SMonitor 0.12.0, the exact case in this report now interpolates:

```python
warn(GpuNotAvailableWarning(reason='the taichi package is not installed'))
```

```
WARNING: GPU acceleration was requested but is not available: the taichi package is not
installed (Hint: The calculation falls back to the CPU kernel ...)
```

`{reason}` renders. The rule this collided with -- pass raw data in `extra` and let
SMonitor interpolate -- is implementable again for warnings routed through `warn()`.

**On the workaround this report mentions:** MolSysMT never applied it. The call sites --
`structure/get_angles.py`, `get_contacts.py`, `least_rmsd_fit.py` -- always passed
`GpuNotAvailableWarning(reason=...)` as structured data, and the catalog entry declares only
code, source, category and level. What the report described was the constraint the upstream
defect imposed, not a hack taken here; checked on 2026-08-08, there was nothing to undo.

**What did need changing:** the pin. MolSysMT's warnings rely on `{reason}` interpolating,
which only happens from SMonitor 0.12.0, so `smonitor>=0.11.6` allowed an installation that
would show users a literal `{reason}`. Raised to `>=0.12.0`.
