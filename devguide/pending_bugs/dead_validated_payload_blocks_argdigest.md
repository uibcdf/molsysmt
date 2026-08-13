---
summary: The ValidatedPayload branch in the coordinates digester is unreachable, and its import blocks ArgDigest from removing the passport.
issue: uibcdf/molsysmt#153
status: open
opened: 2026-08-13
closed:
severity: medium
verification: measured
area: [digestion, dependencies]
blocked_by: []
supersedes: []
---

# Bug: an unreachable passport branch pins a dependency ArgDigest is removing

**Severity:** medium — the code does nothing, but its import is what stops ArgDigest
from deleting a mechanism it has decided to remove.
**Locations:** `molsysmt/_private/argdigest/argument/coordinates.py`,
`molsysmt/_private/argdigest/argument/molecular_system.py`

## The branch

```python
# coordinates.py:1
from argdigest.core.contract import ValidatedPayload
...
# coordinates.py:83
if caller is not None and caller.startswith("molsysmt.lib.structure"):
     return ValidatedPayload(value=q, unit=str(unit),
                             dtype=str(value.dtype), ndim=value.ndim)
```

`molecular_system.py:25` carries the same guard without the payload.

## It cannot fire

ArgDigest builds the `caller` from the module of the decorated callable. For the guard
to be true, a decorated function would have to live under `molsysmt.lib.structure`.

**Static.** Importing the whole package and inspecting every decorated callable:

| | |
| --- | ---: |
| Decorated callables | 26 519 |
| Under `molsysmt.lib.*` | **0** |
| Classes defined under `molsysmt.lib.*` | 1 (`molsysmt.lib.series.serialized_lists`) |
| …of those, with a decorated method, inherited or not | **0** |

The class check matters because for a method ArgDigest resolves the owner from the
*runtime* class, so a subclass under `molsysmt.lib` inheriting a decorated method would
have produced such a caller. None exists.

**Runtime.** The full suite was run against an instrumented copy
(`pytest tests/ --receptor=llm -n 12 -q`, 9932 passed, 11 skipped, 363 s), counting every
time the branch was reached and recording any caller starting with `molsysmt.lib`:

```
trusted=0 passport=0 lib_callers=[]     (in each worker that loaded the module)
```

Zero, and no caller under `molsysmt.lib` was ever seen at all.

## Why it is worth acting on now

ArgDigest is removing `ValidatedPayload` entirely — not repairing it. The mechanism had
two live defects, no users anywhere in the suite, and the one performance problem it was
meant to address turned out to be a placement bug (uibcdf/molsysmt#147). See
`uibcdf/argdigest` → `devguide/solved_bugs/the_passport_is_two_classes_and_admits_too_much.md`.

The import above is the only thing standing in the way. Because digester discovery is
package-style, ArgDigest imports **every** module in
`molsysmt._private.argdigest.argument`, so the moment `argdigest.core.contract` is gone
this import raises and **every MolSysMT call fails**:

```
ModuleNotFoundError: No module named 'argdigest.core.contract'
```

Confirmed by running it. In an editable-installed environment this is immediate for
everyone sharing it, so the order is not negotiable: **MolSysMT drops this first, then
ArgDigest removes the passport.**

## Recommended correction

Delete the import and the two guards. Nothing replaces them: internal callers that want
to skip digestion already have `skip_digestion=True`, which measures 7.5 µs against
65.6 µs on a real digester — cheaper than the passport ever was.

If the intent was that `molsysmt/lib/structure` functions *should* be decorated and
never were, that is a separate decision and belongs with #147, which already covers
where digestion should sit.

## Acceptance

The existing suite passing after the deletion is most of it. A guard is only worth
adding if the `molsysmt.lib` trusted path is deliberately kept for later, in which case
it should be a test asserting that at least one decorated callable lives there — the
absence of which is exactly what made this dead.
