---
summary: Empty interaction registry validates transient structure axes during updates
issue: uibcdf/molsysmt#290
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: high
verification: reproduced
area: [native, structure]
guard: tests/basic/iterator/test_iterator.py
normative:
blocked_by: []
supersedes: []
---

# Empty interaction registry validates transient structure axes during updates

**Reported:** 2026-10-02, during the complete local suite after merging Interactions
and current remote main into `03b3185497426676ba4a7d10b05351952401881b`.
**Status:** Resolved in `a50daad4a`; the complete local suite passed 11,699 tests
with 11 existing environment skips. The extra tools/doctest suite passed 259 tests.

## What

`MolSys.interactions` fails with `StructuralInconsistencyError` while an iterator
replaces several structural series in sequence, even when there are no analyses.
The full run passed 11,661 tests and failed 23; seven failures involved this path.

```bash
python -m pytest --receptor=llm tests/basic/iterator/test_iterator.py tests/_private/test_backend_output.py
```

## How

`MolSys._validate_interactions` obtains the structure-axis length before iterating
an empty mapping. During coordinated replacement, old box/time series can still
have the previous chunk length. Geometry setters access this mapping to decide
whether attached analyses impose an axis constraint.
Return immediately when no analyses exist. Nonempty registries retain all
participant, structure, type and name validation.

## Why

The defect breaks ordinary native iteration and geometry setters for systems
without any interactions; it is not restricted to the new detector workflows.

## What was refuted

Changing iterator output shapes or disabling structural consistency is unnecessary:
there is no interaction domain to compare for an empty registry.

## Scope and acceptance

The iterator and backend-output regression tests must pass, alongside the tests
that reject misaligned nonempty registries and invalidate attached observations.
The correction does not make inconsistent structural series valid for other APIs.

## Provenance

Linux x86_64, Python 3.13.14, local editable suite environment, 2026-10-02.
The recorded full-suite command used 12 xdist workers and loadfile distribution.

The integrated checkpoint is recorded in
[the dated validation artifact](../../../devtools/data/interactions_main_integration_20261002.json).
