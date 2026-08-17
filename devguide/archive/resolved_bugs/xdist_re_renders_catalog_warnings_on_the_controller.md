---
summary: Under pytest-xdist the controller rebuilds catalog warnings as cls(rendered_text), so the template renders around its own output a second time.
issue: uibcdf/molsysmt#158
status: resolved
opened: 2026-08-16
closed: 2026-08-17
severity: low
verification: reproduced
area: [tests, diagnostics]
guard: tests/_private/smonitor/test_xdist_warning_reconstruction.py::test_catalog_warnings_are_not_re_rendered
normative:
blocked_by: []
supersedes: []
---

# Bug: xdist re-renders catalog warnings on the controller

**Status:** resolved here by reshaping the warning classes; the upstream defect remains
**Severity:** low — reporting only; the warnings themselves are correct
**Locations:** `xdist/workermanage.py::unserialize_warning_message` (upstream)

## Problem

Running the suite with `-n 12` reports warning text nested inside itself:

```
UnknownAtomNameWarning x50 | Atom name 'Atom name 'Ar' is not recognized; atom
                             type 'UNK' will be used. Provide an explicit...
GpuNotAvailableWarning x15 | GPU acceleration was requested but is not
                             available: GPU acceleration was requested but is
                             not available: MolSysMT 1.0...
```

A second shape appears in the same run, with the class path glued on:

```
CrossChainCovalentBondsWarning x1 | molsysmt._private.smonitor.warnings.
                                    CrossChainCovalentBondsWarning: Cross-chain
                                    covalent bonds were detected...
```

Serial runs are clean. The two differ by exactly this.

## Cause

`pytest_warning_recorded` fires on the worker; xdist serializes the warning and
the controller rebuilds it:

```python
cls = getattr(mod, data["message_class_name"])
message = cls(*data["message_args"])          # message_args is the original .args
except TypeError:
    message = Warning(f"{module}.{cls}: {message_str}")
```

`CatalogWarning.__init__` ends in `super().__init__(full_message)`, so `.args` is
`(rendered_message,)`. Our subclasses take a *domain* field first positionally,
so the controller calls e.g. `UnknownAtomNameWarning(rendered_message)` and the
rendered text lands in `atom_name`, which the catalog template then wraps again.

Reconstructing the 15 catalog warning classes this way gives three outcomes:

| outcome | count | example |
|---|---:|---|
| re-renders the text into a domain field | 5 | `UnknownAtomNameWarning`, `GpuNotAvailableWarning` |
| `TypeError` → generic prefixed fallback | 7 | `CrossChainCovalentBondsWarning` |
| round-trips correctly | 3 | `StructuralAttributeDropWarning` |

It is not SMonitor and not the call sites: we pass
`extra={"atom_name": atom_name}` exactly as `SMONITOR_GUIDE.md` §3.3.1
prescribes, and `pytest-receptor` only reads `str(warning_message.message)`.

## Why it appeared now

Before smonitor `dd54a9b`, `DiagnosticBundle.warn()` emitted the catalog event
and returned without raising a Python warning, so nothing crossed the process
boundary. Restoring standard warning semantics is what exposed this.

## Guard

`conftest.py` wraps `unserialize_warning_message` and keeps the reconstruction
only when it round-trips: if `str(rebuilt) != message_str`, the correct text the
worker already computed is used instead. `category` is rebuilt from its own
fields upstream, so the real class survives either way. With the guard, `-n 12`
output is identical to serial.

The guard also covers the quiet case in the third row above: a subclass whose
parameters all have defaults reconstructs without error but with the *default*
message, which is wrong without looking wrong.

It installs itself only while the defect is present. `conftest.py` probes the
installed xdist first — a real catalog warning through
`serialize_warning_message` and the unpatched `unserialize_warning_message` —
and re-rendering is told apart from every other outcome by the type that comes
back. Watching the reported text instead would never work: the guard normalises
it either way, so a fixed xdist and a broken one look identical downstream.

`test_the_xdist_workaround_is_still_needed` fails the day the probe says the
defect is gone, and its message carries the removal steps. A warning was tried
first and does not survive: raised during `pytest_configure`, it is emitted
before pytest installs its capture and never reaches the report.

## Acceptance

Remove the guard when a released `pytest-xdist` no longer rebuilds warnings this
way. The fix is proposed upstream as `pytest-dev/pytest-xdist#1372`: keep the
rebuilt instance only when it still says what the original said, otherwise take
the fallback xdist already has for warnings it could not recreate. The test that fails if the defect returns is any parallel run of
`tests/element/atom/test_get_atom_type_from_atom_name.py` whose reported warning
text differs from the serial run's.


## Resolution

Fixed in `1cf763f8d` by changing the classes rather than by defending against
the rebuilder. `message` is now the first parameter of every catalog warning and
the domain fields are keyword-only, so `type(w)(*w.args)` — the call every
rebuilder makes — hands the rendered text back as the message instead of as
`atom_name`, `reason` or `attributes`. It needed `smonitor c30a95d` first, which
stopped folding the resolved hint into `args`: while the base class transformed
its own input, no ordering of the subclass parameters could have made the
rebuild idempotent, and ArgDigest's classes proved it — they already took the
message first and doubled just the same.

The workaround in `conftest.py` is gone, along with the probe that decided
whether to install it and the test that watched for it becoming unnecessary.
That test failed the day the fix landed, which is what it was written to do.
Two older workarounds inside the classes themselves — `if isinstance(attributes,
str)` — are gone for the same reason.

What this does **not** resolve is the upstream defect: pytest-xdist still
transfers only `args` and rebuilds by calling the class, so a warning whose text
depends on state that `args` does not carry still arrives degraded. One of ours
does: a hint interpolating a field re-renders with the field missing. That is
`pytest-dev/pytest-xdist#1372`, and it is theirs to close.

Guard: `tests/_private/smonitor/test_xdist_warning_reconstruction.py::test_catalog_warnings_are_not_re_rendered`.
