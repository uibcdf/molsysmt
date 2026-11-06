---
summary: Box factory accepts degenerate dimensions and returns nonfinite cells for incompatible angles.
issue: uibcdf/molsysmt#605
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

# Box factory accepts degenerate dimensions and returns nonfinite cells for incompatible angles

## What

Box factory accepts degenerate dimensions and returns nonfinite cells for incompatible angles. This native scientific boundary is required by the molecular-tools
work under #421 / PR #543 and uibcdf/molsysviewer#264.

## How

Factory [2,3,4] nm and [10,10,170] degrees returns a matrix with NaN. Zero lengths and [0,90,90] angles return singular matrices; negative lengths are accepted. Orthogonal [2,3,4]/[90,90,90] is a finite determinant-24 control. Public native reproduction: `/tmp/msv-box-domain-probe-20261106.log`, source ed09f6453. This is distinct from #465 default angles and #358 units/documentation.

## Why and acceptance

Define and enforce the public physical domain or provide supported native validation for consumers. Retain valid unit/shared-angle/empty-axis semantics and add scientific invalid-input tests. The GUI cell editor remains required, pending this owner contract; no formula/private scientific helper is copied into the addon.

Native scientific fixes and tests belong to the owning team. This contribution
records the observation and bounded consumer admission, not a native repair.
Owner integration, exact-source/installed qualification and postponed human
acceptance remain separate. Neither 1.0 publication is authorized.
