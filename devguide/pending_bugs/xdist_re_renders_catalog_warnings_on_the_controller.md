---
summary: Under pytest-xdist the controller rebuilds catalog warnings as cls(rendered_text), so the template renders around its own output a second time.
issue:
status: guarded
opened: 2026-08-16
closed:
severity: low
verification: measured
area: [test-tooling, diagnostics]
guard: conftest.py::_guard_xdist_warning_reconstruction
normative:
blocked_by: []
supersedes: []
---

# Bug: xdist re-renders catalog warnings on the controller

**Status:** upstream defect in `pytest-xdist`, guarded locally in `conftest.py`
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

## Acceptance

Remove the guard when a released `pytest-xdist` no longer rebuilds warnings this
way. The test that fails if the defect returns is any parallel run of
`tests/element/atom/test_get_atom_type_from_atom_name.py` whose reported warning
text differs from the serial run's.
