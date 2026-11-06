---
summary: Periodic wrapping uses Cartesian diagonal paths for rotated orthogonal row-vector boxes.
issue: uibcdf/molsysmt#607
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [pbc, molsysviewer]
guard: tests/pbc/test_general_cell_wrapping.py
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

## Owner resolution and final source receiving — 2026-11-06

Primary and centered-primary wrapping now use the full inverse of the supplied
row-vector basis. Only genuinely Cartesian-aligned cells use the diagonal fast
path; public geometric orthogonality remains basis-independent. MIC and covalent
reconstruction reuse the existing distance-family reduced-cell primitive instead
of retaining a separate local 27-image search. Cell preparation is outside the
atom loop in the whole-system Rust kernels. No duplicated scientific formula or
consumer-side lower-triangular restriction is needed by the corrected native API.

The guard checks the original literal [5,6,7] case, dense rotated orthogonal and
triclinic cells, primary/centered/MIC routes, selected structures [2,0], both
mutation modes, component reconstruction and nm/pm/m policies against independent
NumPy inverse/wide-lattice truth. The governed scientific registry additionally
checks literal primary/nearest images under non-default units.

The original 63-case orientation/temporal profile has 48 failures and 15 positive
controls before repair. An expanded draft later has two SI-unit failures at an
exact primitive face: conversion roundoff chooses an adjacent periodically
equivalent image. Those failures are retained. Cross-unit nonboundary assertions
now use nonboundary inputs, while the literal face kernel guard and actual
temporal tie controls remain. No tolerance was relaxed, and no near-zero origin
replacement was introduced. Documentation explains the discontinuity.

Implemented in `3eb720444b97f77f9325acf52f55114ece0b5f9e`. The joint native/composition/PBC/
vector/distance/interactions/H5MSM selection passes **5,435 cases**, with zero
failures/errors/skips. The final PBC/docstring/documentation and evidence-runner
profile passes **1,195 cases**, including the final strengthened trajectory
fixtures. The scientific certificate passes **97 cases across 64 registered
nodes**, with zero skips. All **82 Rust unit tests** pass. These scopes overlap
and are local receiving, not installed/platform or release qualification.

The [portable phase-two receipt](../../../devtools/data/pre_1_0_robustness_phase2_receiving_20261106.json)
records exact source/backend identities, original failures, retained warnings,
test chronology and limitations. The initial integrated command used a
nonexistent test path and executed zero cases; it is preserved as unsuccessful
evidence, with the controlled exit-4 diagnostic and corrected-path exit-0 run.
All eight edited notebooks preserve code, outputs, IDs and metadata; only
Markdown changes. Human autosummary edits remain outside these commits.

The native extension is deliberately rebuilt from the delivered Rust sources;
its SHA-256 is `2f1f69f6e0539bd31ee419ec3b7a4deaab20f09045ce3e6504369c9130438525`.
No environment or optional dependency is replaced. Public source verification
and issue synchronization follow this prepared closeout; Viewer graphical
receiving, installed artifacts and the release gate remain separately due.
