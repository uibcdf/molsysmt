---
summary: Periodic wrapping uses Cartesian diagonal paths for rotated orthogonal row-vector boxes.
issue: uibcdf/molsysmt#607
status: open
opened: 2026-11-06
closed:
severity: high
verification: reproduced
area: [pbc, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Periodic wrapping uses Cartesian diagonal paths for rotated orthogonal row-vector boxes

## What

Periodic wrapping uses Cartesian diagonal paths for rotated orthogonal row-vector boxes. This native scientific boundary is required by the molecular-tools
work under #421 / PR #543 and uibcdf/molsysviewer#264.

## How

Native ed09f6453 public wrap_to_pbc/wrap_to_mic, compact=False, box rows [[0,3,0],[-4,0,0],[0,0,5]] nm, point [5,6,7] nm returns [5,6,2] for both. Row-vector primary wrapping gives [-3,0,2]; nearest image gives [1,0,2]. The box determinant is +60. Logs `/tmp/msv-rotated-cell-far-probe-20261106.log` and `/tmp/msv-rotated-cell-probe-20261106.log` retain controls. Closed #257 fixed a different MIC/distance dispatcher, not this PBC family.

## Why and acceptance

Support valid general row-vector cells or reject unsupported orientation before publication. Cover centered-primary/MIC/vector/temporal/component paths, rotated bases, units, order and atomicity against lattice truth. GUI temporarily admits exact lower-triangular matrices only, without tolerance/reorientation; the full general-cell family remains required.

Native scientific fixes and tests belong to the owning team. This contribution
records the observation and bounded consumer admission, not a native repair.
Owner integration, exact-source/installed qualification and postponed human
acceptance remain separate. Neither 1.0 publication is authorized.
