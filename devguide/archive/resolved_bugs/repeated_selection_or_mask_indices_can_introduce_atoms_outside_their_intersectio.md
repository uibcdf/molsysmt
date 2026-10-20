---
summary: Repeated selection or mask indices can introduce atoms outside their intersection.
issue: uibcdf/molsysmt#389
status: resolved
opened: 2026-10-20
closed: 2026-10-20
severity: high
verification: reproduced
area: [selection, basic]
guard: tests/basic/select/test_duplicate_mask_indices.py
normative:
blocked_by: []
supersedes: []
---

# Duplicate indices corrupt selection-mask membership

## What

While implementing uibcdf/molsysmt#206, a literal selection-mask control finds
that duplicates may introduce atoms outside the requested intersection:

```python
import molsysmt as msm
from molsysmt.native import MolSys
msm.select(MolSys(n_atoms=3), selection=[0], mask=[1, 1])
# Before repair: [1]; correct set intersection: []
```

Both axes are in range, but atom 1 is outside the selection. Repetition can
also duplicate valid output members. The defect affects direct select calls
and consumers delegating masked selection; it is not limited to summary tables.

## How

The shared mask path passed assume_unique=True to numpy.intersect1d without
establishing uniqueness. NumPy's resulting adjacent-equality algorithm can
mistake repetitions within one input for membership in both inputs.

## Why

Incorrect masks can include unrequested atoms and corrupt downstream molecular
queries. Repair the selection owner rather than deduplicating only info inputs.

## What is measured and what is assumed

All four explicit duplicate-membership guards fail before repair. After repair,
148 combined info/selection cases pass on Python 3.14.7 with twelve workers and
pytest-receptor; existing legacy H5MSM warnings remain visible. No performance
improvement is claimed.

## What was refuted

Input range validation does not establish uniqueness. The two separate inputs
may each contain valid repeated indices. A consumer-only workaround would leave
other public select/get consumers exposed to the same shared intersection.

## Resolution

Use NumPy's ordinary set-intersection contract, without the unsupported
uniqueness assumption. The output is sorted and unique whenever a mask is
active. Unmasked ordering and repetitions remain unchanged. The guards compare
literal expected outputs and independent Python set intersections, including
repetition confined to only one input. Existing selector behavior and failure
controls remain intact. This adds no dependency or alternative selector.

## Scope and exclusions

Repairs the existing select mask intersection. Does not change the semantics of
unmasked selections, chemical states, attribute queries or stored indices.
The separate info mask extension is tracked in uibcdf/molsysmt#206.

## Provenance

2026-10-20, Linux, existing Python 3.14.7 development interpreter. Original
source context: 94e579356. Before/after logs are retained locally, not committed.
