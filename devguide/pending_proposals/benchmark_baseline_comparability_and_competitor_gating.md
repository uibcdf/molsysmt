---
summary: Define comparable performance baselines and third-party gate semantics.
issue: uibcdf/molsysmt#567
status: partial
opened: 2026-11-04
closed:
verification: measured
area: [ci, performance]
guard: devtools/tests/test_benchmark_comparison.py
normative: devguide/benchmarking/performance_policy.md
blocked_by: []
supersedes: []
---

# Benchmark baseline comparability and competitor gating

**Reported:** 2026-11-04, with explicit maintainer authorization, while receiving
PR #543 under uibcdf/molsysviewer#264.
**Status:** partial implementation. The maintainer has accepted advisory timing
for both product and third-party observations; full comparability remains open.

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

## Independent malformed-data findings — 2026-11-08

Three tiny controls on unchanged comparer `fbafc69a5` return exit 0 for empty
sessions, missing reference measurements and a NaN median. These are false
numeric successes independent of the unresolved product/control blocking
decision. Original source, input hashes and output are retained in private
receiving. A scoped correction rejects invalid/empty records, nonfinite or
nonpositive medians, absent reference measurements and invalid thresholds
before comparing. It preserves the default 15 percent limit and every matched
third-party blocking path. New paths without reference remain explicitly
unassessed. The script does not claim environment/workload comparability.

The owner has been asked asynchronously whether direct external measurements
should remain blocking or serve as informational controls. Until that answer,
the existing scope is preserved. Original failed campaigns/medians are not
relabelled, no baseline is renewed and no benchmark computation is run. This
stdlib-only saved-JSON developer route adds no optional molecular engine,
unit-policy mutation, scientific attribution or product API boundary. Full
metadata/role/artifact and owner acceptance remain pending; this issue is not
closed by the malformed-data correction.

## Scoped numeric-data receiving — 2026-11-08

`e21cd13419ccedcc7ebebd7aef1bb1e7c585f34a` passes 45 semantic cases
and fourteen fast gates on clean source. The
[receipt](../../devtools/data/benchmark_data_receiving_567_20261108.json)
retains the original three false-success controls, source/input hashes and
bounded receiving. The guard rejects empty, absent, malformed and nonfinite
numeric evidence while preserving real regression detection and the original
15 percent and matched-third-party scope. This does not establish comparable
workloads/environments, accept an owner policy, renew a baseline or close #567.

## Session evidence and reference ownership — 2026-11-08

`12a6c6fc2` adds explicit `run_matrix.py --output` and per-campaign owned
reference files. A tiny original orchestration control proves that the old
runner removes a pre-existing caller `solvated_villin.pdb`; the new independent
ownership/failure controls preserve it. CI writes current data separately from
the reference and is configured to retain the raw JSON, source identity and
native-status-preserving logs after failures. Actual hosted upload remains
unexecuted; a local YAML/shell guard is not an upload certificate.

The [receiving record](../../devtools/data/benchmark_evidence_receiving_567_20261108.json)
retains all prototype failures, the real original reference-file control,
59 passing benchmark cases and the separate #653 selector correction. Clean
joint receiving passes 104 cases. The original default 15 percent, matched
third-party blocking scope, failed medians and reference bytes are unchanged.
No timing matrix or reviewed baseline renewal is performed. Compatibility
metadata and the explicit owner product/control-role decision remain open;
this is partial work and does not complete #567's audit milestone.


## Maintainer decision — 2026-11-09

Diego rejects restricting a scientifically correct implementation because it
is slower than a third party. This also makes own-version timing observations
advisory: consistent comparable inefficiency above the default 15 percent
threshold is a reason for an improvement issue, not scientific API withdrawal
or implementation rejection. Differences within that margin generally require
no efficiency issue. Numerical correctness and data-integrity controls retain
their mandatory roles.

The [accepted policy](../benchmarking/performance_policy.md) records this
disposition. The comparer now warns rather than returns a regression failure
for valid slower timings. Malformed/incomplete records still fail diagnostically
and never claim performance approval; the performance job is explicitly advisory,
retaining those native failures and original artifacts. Product and external
paths both receive this policy. Existing historical failed runs and reference
bytes remain unchanged. New workload/environment comparability metadata, its
validation, repeated-measurement interpretation and reviewed baseline renewal
remain outstanding; no attributed product slowdown is established by this
policy change or the old direct-MDTraj observation.


## Accepted advisory implementation receiving — 2026-11-09

Clean d1cf23362 receives all 121 affected comparer/evidence/reference/certificate/
addon preflight controls and all fourteen fast gates. The [policy receiving record](../../devtools/data/advisory_performance_policy_receiving_567_20261109.json)
retains the synthetic old blocking policy, new warning assertions for product
and external paths, invalid-data refusals, actual shell-pipeline failures and
unchanged reference bytes. A temporary profile selected the same policy suite
twice; both attempts remain distinct, without counting them as 242 unique tests
or as fast-gate coverage. The actual fast gates run separately. Full repository
Ruff and developer-guide/index validation pass. The scientific product, backend,
public docs and numeric tests remain byte-identical to c37e42510. No timings are
measured anew and no original failure is rewritten. Comparability and reference
renewal remain open, so #567 stays partial.


## Complete contract implementation under receiving — 2026-11-09

The [comparable-session contract](../benchmarking/comparable_sessions.md) now
defines and implements known runtime/provider/hardware/resource/unit identities,
actual input/observable/precision descriptors, raw repetitions and matched timing
protocols. Product revisions may change; changed environments or workloads cannot
masquerade as regressions. Structured partial/unevaluable reports retain native
diagnostic failures while the timing job stays advisory. Provider initializer
origins/hashes and retained package/build records prevent version labels alone
from certifying an imported source. This is declared correspondence, not
authentication or a statistical/causal guarantee. The original reference remains
unchanged and explicitly historical; renewal is a separately reviewed action.

Numerical prechecks expose independent #673 (fitted/unfitted RMSD, PBC mismatch,
and a SciPy call labelled MDTraj). Complete tiny production exposes #676's
inherited-worker hang. Both corrections retain original controls and failures,
use full shared unit standards, and prepare competitive cases in fresh
interpreters without serializing native objects. Dirty directed receiving now
passes 123 comparison/observable controls, ten actual tiny-campaign/runtime
controls and nine worker lifecycle controls; overlap is not unique coverage.
A complete clean-source collection and fast gates remain due before closure.

New incoming #674 (late Pint-cache setup) and #675 (regenerated-index composition
warning) are independent consumer reports; reproduce them after this finite
receiving block. Neither demonstrates new molecular data loss. No package,
release, historical-baseline renewal or remote workflow is launched here.
