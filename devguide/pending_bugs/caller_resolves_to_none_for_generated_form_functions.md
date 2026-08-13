---
summary: Generated form functions carry no __module__, so digestion sees caller="None.<name>" for 16% of the decorated surface.
issue: uibcdf/molsysmt#152
status: open
opened: 2026-08-13
closed:
severity: high
verification: measured
area: [form, digestion, diagnostics]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: `caller` resolves to `None` for generated form functions

**Severity:** high — caller-dependent digestion is silently inert across 16% of the
decorated surface, and the tests barely reach it.
**Locations:** the generated form functions (`molsysmt/form/MDAnalysis_Topology`,
`molsysmt_TopologyDict`, `file_topology_yaml`, `molsysmt_MolSysDict`,
`file_molsys_yaml`, `file_structures_yaml`)
**Found:** 2026-08-13, while verifying an unrelated claim about `molsysmt.lib`.

## Symptom

```python
from molsysmt.form import MDAnalysis_Topology as m

m.get_atom_id_from_atom.__module__      # None
```

ArgDigest builds the `caller` a digester receives as
`f"{owner_module}.{fn.__name__}"`, so for these functions it is the string
**`"None.get_atom_id_from_atom"`**.

## Scope

Measured by importing the whole package and inspecting every decorated callable:

| | |
| --- | ---: |
| Decorated callables | 26 519 |
| With `__module__` unset, so `caller="None.…"` | **4 324 (16%)** |

| Form | Affected |
| --- | ---: |
| `molsysmt.form.MDAnalysis_Topology` | 976 |
| `molsysmt.form.molsysmt_TopologyDict` | 976 |
| `molsysmt.form.file_topology_yaml` | 976 |
| `molsysmt.form.molsysmt_MolSysDict` | 678 |
| `molsysmt.form.file_molsys_yaml` | 678 |
| `molsysmt.form.file_structures_yaml` | 40 |

Hand-written forms are unaffected: `molsysmt_MolSys.has_attribute` reports
`molsysmt.form.molsysmt_MolSys.has_attribute` correctly.

## Cause

Following the wrapper chain to the bottom:

```
[0] __module__=None   code=decorator.py   (smonitor's signal wrapper)
[1] __module__=None   code=<string>       (the generated function itself)
```

`co_filename` is `<string>`, so the innermost function is built by `exec()` over
generated source. The namespace that `exec` runs in carries no `__name__`, so the
function is created without a `__module__`, and every wrapper above it copies that
`None` upward through `functools.wraps`.

## Why it matters

1. **Caller-aware digestion is silently inert for these functions.** 102 of MolSysMT's
   392 digesters branch on `caller`. For an affected callable every such branch sees
   `"None.…"`, matches nothing, and falls through to the default — without any
   diagnostic, because falling through is a legitimate outcome.
2. **The function argument contract cannot resolve them.** Axis 1 matches an exact
   caller or an `fnmatch` pattern against the caller string. Neither can name a function
   whose caller is `"None.<name>"`, so a contract declared for one of these forms would
   never apply.
3. **Diagnostics name them wrongly.** An `ArgumentError` raised inside one of these
   reports `None.get_atom_id_from_atom` as the origin, which points nowhere.

## How exposed it is today

The full suite was run instrumented (`pytest tests/ --receptor=llm -n 12 -q`, 9932
passed, 11 skipped, 363 s), wrapping ArgDigest's owner resolution to count:

| | |
| --- | ---: |
| Digested calls | 211 448 |
| With owner `None` | **57 (0.03%)** |
| Distinct callables reached | 17 |

**The gap between 16% of the surface and 0.03% of the calls is part of the finding.**
The tests barely exercise these paths, so a caller-dependent regression in a generated
form would not be caught. The low runtime number is not reassurance; it is a measure of
how little the affected surface is tested.

## Reproduction

```python
import importlib, pkgutil, sys
import molsysmt

for mi in pkgutil.walk_packages(molsysmt.__path__, "molsysmt."):
    try:
        importlib.import_module(mi.name)
    except Exception:
        pass

total = broken = 0
for name, mod in list(sys.modules.items()):
    if not isinstance(name, str) or not name.startswith("molsysmt") or mod is None:
        continue
    for obj in vars(mod).values():
        if callable(obj) and hasattr(obj, "digestion_plan"):
            total += 1
            if not (getattr(obj, "__module__", None) or ""):
                broken += 1

print(total, broken)          # 26519 4324
```

## Recommended correction

Set the module on the generated function. Either seed the `exec` namespace with
`__name__` set to the target module, or assign `fn.__module__` immediately after
creation and before decoration — the decorators copy it, so it has to be right before
they run.

Worth checking in the same pass whether `__qualname__` is right for these: it is the
bare name today, where a hand-written form carries the dotted path.

## Acceptance

A test that fails if the defect returns: assert that **every** decorated callable in the
package reports a non-empty `__module__`. It is a single pass over the imported package,
it names the offenders when it fails, and it cannot rot the way a per-form check would.

## Relationship to uibcdf/molsysmt#147

Different cause, different area, and this one is worse. #147 is about digestion being
placed on internal predicates and costing time. This is about digestion being given the
wrong identity and silently doing nothing. They were found in the same investigation and
should not be merged: the fix for one does not touch the other.
