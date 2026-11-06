---
summary: Temporal unwrap reuses the first box classification after later cells become triclinic.
issue: uibcdf/molsysmt#606
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

# Temporal unwrap reuses the first box classification after later cells become triclinic

## What

Temporal unwrap reuses the first box classification after later cells become triclinic. This native scientific boundary is required by the molecular-tools
work under #421 / PR #543 and uibcdf/molsysviewer#264.

## How

On native ed09f6453, boxes diag(3,4,5), B, B with B rows [[3,0,0],[2,4,0],[0,0,5]], selected atom positions [0,0,0], [0,0,0], [1.9,3.8,0] nm produce [-1.1,-0.2,0] at the third sample. Lattice enumeration gives [-0.1,-0.2,0]; observed shift coefficients [1/3,1,0] are nonintegral. All-B control is correct. `/tmp/msv-unwrap-changing-cell-probe-20261106.log` retains the reproduction. Current Rust chooses orthogonality once for the trajectory.

## Why and acceptance

Classify the actual transition box or reject unsupported changing-cell inputs before writes; document previous/current box semantics. Qualify direction changes, ordering, units and atomicity. The GUI temporarily admits identical selected boxes only; general variable-cell support remains required and the expert wrapper stays native.

Native scientific fixes and tests belong to the owning team. This contribution
records the observation and bounded consumer admission, not a native repair.
Owner integration, exact-source/installed qualification and postponed human
acceptance remain separate. Neither 1.0 publication is authorized.
