---
summary: Periodic box nonsingularity depends on application length units.
issue: uibcdf/molsysmt#619
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [pbc, units]
guard: tests/pbc/test_small_periodic_origins.py::test_box_nonsingularity_admission_is_invariant_under_length_units
normative:
blocked_by: []
supersedes: []
---

# Periodic cell admission uses a dimensional determinant cutoff

## What

The shared raw-cell validator compares `abs(det(box))` with float64 epsilon,
without accounting for the numeric length unit. A 3/4/5-nm cell with an atom at
x=3.1 nm wraps to x=0.1 nm under nm but rejects as singular under meters.
A 1e-6-nm cube similarly rejects under nm and succeeds under angstrom/pm.

## How

Public primary/MIC/unwrap regressions produce three failures and six positive
controls for the small cube before the correction. A second controlled public
probe selects the exact validator from `a91a4fd1b` or its correction, leaving the
same current kernel in place. The ordinary 3/4/5-nm cell succeeds under nm with
both validators, fails under m with the original and succeeds under m with the
correction. The failure precedes numerical wrapping. The local JSON probe is
`.pytest_cache/pre1-review-20261106/dimensional-box-validation-probe.json`.

The correction normalizes each nonzero finite cell by its maximum absolute
entry before comparing the absolute dimensionless determinant with float64
machine epsilon. Shape, structure-count/broadcast, finite and genuine-singularity
checks remain. Either handedness remains admitted; this is not the positive-
length convention of the canonical cell factory. No application policy is
changed. The stricter existing compound-participant validator already uses a
normalized determinant and retains its separate admitted conditioning limit.

## Why

A determinant is a volume. A fixed numeric threshold on that dimensional value
changes physical admission under a supported unit policy. This is a separate
mechanism from #608's small-origin replacement and #605's constructor domain,
with receiving shared in the same PBC quantity-invariance milestone.

## Acceptance and receiving

Cover ordinary/small cells across nm, angstrom, pm and m, primary/MIC/unwrap,
and both handedness choices. Preserve shape/broadcast/nonfinite/singular guards.
Keep the original failure evidence and publish the corrected native source.
No new method, dependency, unit policy or file schema is added.

The original 626-case PBC/scientific receiving already includes the first nine
cases after the correction. Expanded ordinary/meter/handedness receiving follows
in the joint phase-two certificate. This additional demonstrated defect is
admitted under the existing scope rule, without awarding extra progress points
or expanding deferred scientific coverage.

## Provenance

Linux/Python 3.14.7, existing development environment, published Pytest Receptor
1.2.1 and 12 workers. The Rust backend is intentionally rebuilt for #607/#606;
this validator correction itself is Python-side and does not change a kernel.
Complete issue acquisition before filing: seven pages, 550 issues, 102 open;
no matching dimensional-singularity report is present. Public-source and
installed/platform/release receiving remain distinct.

## Owner resolution and final source receiving — 2026-11-06

The shared validator now tests the absolute determinant after per-cell
maximum-entry normalization against float64 epsilon. Genuine singularity,
finite/shape/count/broadcast checks and either-handed raw bases are preserved.
The stricter existing compound-participant conditioning contract remains a
separate feature boundary; no unreviewed common tolerance is imposed.

The final independent 48-case guard covers ordinary 3-nm and small 1e-6-nm cells,
nm/angstrom/pm/m policies, primary/MIC/unwrap and both handedness choices. The
original nine-case probe has three failures and six passing controls; the
separate controlled ordinary-cell probe retains the exact public validator from
a91a4fd1b and isolates rejection before any numerical wrapping. Neither probe
claims execution of an entire old runtime with a new kernel.

This is a native quantity-integrity correction, not a new physical model,
application standard or file schema. Its acceptance shares #608's existing
five-point milestone; opening a separate issue does not inflate plan progress.

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
