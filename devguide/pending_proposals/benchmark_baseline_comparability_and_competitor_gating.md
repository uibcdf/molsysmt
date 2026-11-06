---
summary: Define comparable performance baselines and third-party gate semantics.
issue: uibcdf/molsysmt#567
status: open
opened: 2026-11-04
closed:
verification: measured
area: [ci, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Benchmark baseline comparability and competitor gating

**Reported:** 2026-11-04, with explicit maintainer authorization, while receiving
PR #543 under uibcdf/molsysviewer#264.
**Status:** open proposal for the owning team's benchmark/CI contract decision.

## What

Run 41949690963, attempt 2, completes measurements and fails solely on
`competitor_center_mdtraj`: 1434.73 μs baseline versus 1895.41 μs current,
+32.11%, exceeding the unchanged 15% threshold. All measured MolSysMT paths
improve (approximately -16.67% to -42.02%). The cause of the MDTraj delta is
not established; the result is not a passing performance gate.

Define which baseline/workload/environment combinations are comparable and
which third-party measurements block product regression acceptance versus
serve as competitive observations or calibration controls. Preserve the current
failure and threshold until the owner accepts a policy; do not rerun until green.

## How

`.github/workflows/benchmarks.yml` selects Python 3.14, extracts the main-branch
`benchmarks/baselines/competitor_matrix_session.json` and runs
`benchmarks/compare_runs.py` with `--threshold 0.15`. The historical reference
records Python 3.13.14, Linux `7.0.0-28-generic`, commit
`f9dd4b0b62f76b1cc878fea83b5f6e51617a5263`, `git_dirty=true` and MolSysMT
`0.21.0+325.g7cedab74a.dirty`, generated 2026-09-01. The current workflow uses
a hosted Azure Linux runner and the new source environment.

The comparer checks medians for matching names without assessing environment
or workload compatibility. Existing telemetry does not capture all dependency,
CPU and thread details needed to assess that compatibility. The workflow does
not retain the new complete session JSON as an artifact after failure; only
its printed summaries survive. The proposed route is explicit metadata,
reviewed baseline renewal and fail-closed comparability checks, retaining
original medians and any real regression assertion required by the owner.

## Why

The gate currently blocks a contribution whose benchmark/scientific code and
third-party declarations are unchanged, solely on the competitor delta. This
neither proves that the addon regressed nor proves measurement noise. A useful
gate must separate product regressions, comparator/environment changes and
insufficient evidence. Benchmarking remains owned by MolSysMT; no consumer
threshold change or native scientific workaround is proposed.

## Measurements and uncertainty

The values and outcome above come from the original public job log. The
reference environment is read from the committed JSON. Hardware load, dependency
or interpreter effects and causal attribution remain unverified. This is a
comparability/governance review, not a declaration that the current gate is waived.

Attempt 1 separately failed during Conda repodata transfer before benchmarks.
Attempt 2 recovered provisioning, executed measurements and failed the numeric
audit. Both remain distinct historical outcomes. Smoke 41949691156 attempt 2
passes independently; a passing functional run is not a performance certificate.

## Later source observation — 2026-11-04

Parent source `53d90adc0` run 41956040841 passes with all benchmark/audit steps
executed. The next source `2d1923996` run 41958120472 fails solely on the same
MDTraj centering metric: 1434.73 μs baseline, 1700.76 μs current, +18.54%, with
the unchanged 15% threshold. Both are ordinary new-source campaigns, without a
manual retry or benchmark-policy change. Preserve each conclusion and its
original input; the later failure does not establish its cause or waive the
comparability decision. Native logs and receptor manifests are retained in the
consumer receiving record. This observation adds no claim that all other native
measurements improved in that run.

## Acceptance criteria

Retain complete session JSON/provenance on successful and failed runs. Define
required workload dimensions, units/dtypes, engines/dependency identities,
CPU/thread settings, warm-up/repeats and dispersion. Add pytest guards for the
accepted comparison and metadata contract, including incompatible/missing
baselines and missing measurements, while preserving legitimate regression
detection. Any change to blocking scope or thresholds requires the owner's
explicit decision and durable contract, not assertion removal to obtain green CI.

## Provenance

Source `ee1153d983a37416eaee85710c5b97e0acb2ecc1`, PR #543; run
[41949690963](https://github.com/uibcdf/molsysmt/actions/runs/41949690963), attempt 2.
The native log and GH Run Receptor bundle are retained in Viewer `.pytest_cache`
through receiving, with resource review by 2026-11-11. This proposal qualifies
no package, candidate, scientific method or installed artifact.
