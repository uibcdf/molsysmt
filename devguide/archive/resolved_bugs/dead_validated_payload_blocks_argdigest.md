---
summary: The ValidatedPayload branch in the coordinates digester is unreachable, and its import blocks ArgDigest from removing the passport.
issue: uibcdf/molsysmt#153
status: resolved
opened: 2026-08-13
closed: 2026-08-13
severity: medium
verification: measured
area: [digestion, dependencies]
guard: tests/_private/argdigest/test_no_validated_payload.py
normative: ARGDIGEST_GUIDE.md
blocked_by: []
supersedes: []
---

# Bug: an unreachable passport branch pins a dependency ArgDigest is removing

**Severity:** medium — the code does nothing, but its import is what stops ArgDigest
from deleting a mechanism it has decided to remove.
**Location:** `molsysmt/_private/argdigest/argument/coordinates.py`

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

The same file carried an earlier trusted-array guard for the identical caller
prefix. An earlier version of this report incorrectly attributed that guard to
`molecular_system.py`; inspection of the current tree confirms that both guards
were in `coordinates.py`.

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

Delete the import and the two guards. Retire active documentation and development rules
that present the passport as implemented. Nothing replaces it: internal callers that want
to skip digestion already have `skip_digestion=True`, which measures 7.5 µs against
65.6 µs on a real digester — cheaper than the passport ever was.

If the intent was that `molsysmt/lib/structure` functions *should* be decorated and
never were, that is a separate decision and belongs with #147, which already covers
where digestion should sit.

## Resolution

The import and both unreachable caller guards were deleted without replacement. The
tracked passport sandbox was removed, active development rules and user documentation
now describe only ordinary digestion and explicit caller-owned
`skip_digestion=True`, and historical documents that could otherwise be read as current
implementation claims carry dated corrections.

`tests/_private/argdigest/test_no_validated_payload.py` scans the runtime package and
fails if either `ValidatedPayload` or `argdigest.core.contract` returns. The complete
private-digester test surface passes against both dependency generations:

```text
ArgDigest main before removal:                         372 passed
ArgDigest refactor/remove-the-passport (15aed7c):      372 passed
```

The second run imports MolSysMT with no
`argdigest.core.contract` module present. This proves the required landing order is now
safe: MolSysMT can land first, after which ArgDigest may merge its removal branch. The
repository's fast release gate also passes 12/12 after the removal.

## Acceptance

- No runtime MolSysMT source imports or names the removed protocol.
- MolSysMT imports and the focused scientific-array digesters pass with both the old
  and passport-free ArgDigest trees.
- Active rules and user documentation do not present a value passport as available.
- The absence of the runtime dependency has an executable regression guard.
