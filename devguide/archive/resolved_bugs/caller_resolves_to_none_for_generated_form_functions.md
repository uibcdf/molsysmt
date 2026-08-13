---
summary: Generated form functions carry no __module__, so digestion receives caller="None.<name>".
issue: uibcdf/molsysmt#152
status: resolved
opened: 2026-08-13
closed: 2026-08-13
severity: medium
verification: measured
area: [form, digestion, diagnostics]
guard: tests/form/test_generated_getter_identity.py
normative:
blocked_by: []
supersedes: []
---

# Bug: `caller` resolves to `None` for generated form functions

**Severity:** medium — diagnostics and contract identity are wrong across a large
generated adapter surface, although no incorrect scientific result has been demonstrated.
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
| Decorated callable references | 26 519 |
| Broken references, including re-exports | **4 324 (16.31%)** |
| Distinct decorated callable objects | 13 319 |
| Distinct broken generated functions | **2 162 (16.23%)** |

The original counts below include each function twice: once in its implementation
module and once through the form-package re-export. The number of distinct generated
functions is half each row.

| Form | References | Distinct functions |
| --- | ---: | ---: |
| `molsysmt.form.MDAnalysis_Topology` | 976 | 488 |
| `molsysmt.form.molsysmt_TopologyDict` | 976 | 488 |
| `molsysmt.form.file_topology_yaml` | 976 | 488 |
| `molsysmt.form.molsysmt_MolSysDict` | 678 | 339 |
| `molsysmt.form.file_molsys_yaml` | 678 | 339 |
| `molsysmt.form.file_structures_yaml` | 40 | 20 |

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

1. **Caller-aware digestion cannot identify these functions.** MolSysMT has many
   caller-dependent digesters, but the generated getter signatures currently overlap
   that surface only through `item`; its current caller-specific branch belongs to
   `append_structures`, not these getters. No wrong scientific result is therefore
   claimed. The broken identity would nevertheless make any present or future
   generated-getter-specific branch silently miss.
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

**The gap between 16% of the discovered references and 0.03% of the calls is part of
the finding.**
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

Seed each `exec` namespace with `__name__` set to the generator module. This assigns the
identity before decoration, so wrappers copy it normally. The bare `__qualname__` is
correct for a module-level function and matches hand-written form functions; it must not
be replaced with a dotted module path.

## Acceptance

Tests that fail if the defect returns:

1. import the nine generator modules and assert that every exported generated function
   reports exactly that module's `__name__`;
2. provoke one digester failure and assert that its structured diagnostic carries the
   complete generated-module caller, never `None.<name>`.

Importing every optional module in MolSysMT is not required for this guard. It would
add unrelated dependency side effects and count re-export aliases as separate functions.

## Relationship to uibcdf/molsysmt#147

Different cause, different area, and this one is worse. #147 is about digestion being
placed on internal predicates and costing time. This is about digestion being given the
wrong identity and silently doing nothing. They were found in the same investigation and
should not be merged: the fix for one does not touch the other.

## Resolution — 2026-08-13

All nine generated-getter modules now seed their `exec()` namespace with the
defining module's `__name__` before `@arg_digest` and SMonitor wrap the function.
The resulting 2,162 distinct generated functions carry their exact module
identity, and structured diagnostics name a resolvable caller rather than
`None.<name>`.

The regression guard checks every exported function in all nine modules,
provokes a real `ArgumentError` and inspects its structured caller, and scans
all form sources so a future `exec()`-based ArgDigest generator cannot omit the
module seed. The six affected form families and form-plugin conventions pass
70 tests; the focused identity guard passes 11 tests. No passport or
`ValidatedPayload` behavior changed; uibcdf/molsysmt#153 remains open pending
the independent ArgDigest design decision.
