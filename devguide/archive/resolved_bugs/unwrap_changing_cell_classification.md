---
summary: Temporal unwrap reuses the first box classification after later cells become triclinic.
issue: uibcdf/molsysmt#606
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [pbc, molsysviewer]
guard: tests/pbc/unwrap/test_changing_cells.py
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

## Owner resolution and final source receiving — 2026-11-06

Each transition now prepares the actual previous selected structure's cell.
It uses the full row-vector inverse and shared distance-family MIC calculation
when required, rather than carrying the first structure's classification through
the sequence. Original-basis ties-to-even seeds survive unless the MIC candidate
is strictly shorter. Whole-system temporal traversal remains serial because each
updated coordinate supplies the next transition's reference.

The final guards exercise both actual classification changes, changing lengths,
nonconsecutive traversal in both orders, both mutation modes and non-default
units. Review found that simply reversing [orthogonal,triclinic,triclinic] does
not exercise a reverse classification change in the previous-cell convention;
the final fixture explicitly uses [triclinic,orthogonal,orthogonal] as its second
case. Independent wide-lattice expectations and governed literal displacements
protect the result. Sixteen real public half-cell-jump cases protect ties-to-even.

The docstring, tutorial and common course define previous-cell/traversal semantics
and the sampling assumption. Nearest-image continuity cannot infer a unique
physical winding from structures that undersample a large displacement; unwrap
also does not replace within-structure covalent reconstruction.

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
