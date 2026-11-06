---
summary: Near-zero periodic origins are snapped using application-dependent units.
issue: uibcdf/molsysmt#608
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [pbc, units, molsysviewer]
guard: tests/pbc/test_small_periodic_origins.py
normative:
blocked_by: []
supersedes: []
---

# Near-zero periodic origins and application units

## What

The native atomwise primary wrapping path replaces a near-zero origin using
`np.isclose(..., atol=1e-4)` on standardized numeric values. The physical
threshold changes with the application's length standard, so the same molecular
system and explicit quantity can produce different primary-cell images.

## How

Native ed09f6453, Python 3.14, no Viewer: a selected atom at [0,0,0] nm in a
3/4/5-nm orthogonal cell, with explicit origin [1e-5,0,0] nm and compact=False,
returns [0,0,0] nm under nm/angstrom standards and [3,0,0] nm under pm.
The primary cell starts at x=1e-5 nm, so x=0 is outside that requested cell.
The latter image is consistent with the origin. Reproduction retained in
`/tmp/msv-periodic-origin-policy-probe-20261106.log`.

## Why and acceptance

Preserve explicit reference points without an application-unit-dependent
replacement. Qualify exact zero, small positive/negative origins, boundary atoms,
input quantity units, nm/angstrom/pm policies, grouping, structure scope and
independent/in-place effects. Review related centered/MIC branches without
assuming they share the same failure. Do not mask image differences by a loose
coordinate tolerance or add a consumer-side origin formula/standard override.

This finding keeps general reference-point and periodic release qualification
pending under #421 / PR #543 and uibcdf/molsysviewer#264. The prepared GUI's
passing lattice cases cover their explicit tested origins, not this failed
boundary case. Native correction and exact consumer receiving remain required;
no scientific workaround is implemented in the addon.

## Owner resolution and final source receiving — 2026-11-06

The wrapping owners now preserve every explicit origin/center quantity through
unit conversion. The atomwise primary and MIC routes no longer replace a small
numeric origin with zero. The centered-primary no-op assignment is removed as
well. Component and isolated routes share the same physical reference-point
contract; no application policy or consumer-side formula is imposed.

The first 36-case origin fixture exposed four component failures but missed
atomwise discontinuities. It was strengthened to put atoms near the relevant
boundaries: the original runtime then fails 24 of 108 cases. The corrected tests
cover zero and small signed origins, primary/centered/MIC, atom/component modes,
selected structures, both mutation modes and nm/angstrom/pm policies. A governed
literal primary-cell image also passes under meters. These are physical image
checks, not agreement between two wrappers sharing one implementation.

#619 separately corrects a dimensional singularity cutoff discovered while
expanding this receiving. Its own report/guard remains distinct; both contribute
to the same unit-invariance milestone under #334.

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
