---
summary: Restore current Codecov evidence before reintroducing the coverage badge.
issue: uibcdf/molsysmt#286
status: partial
opened: 2026-10-01
closed:
verification: measured
area: [governance, ci, coverage]
guard: devtools/tests/test_nightly_full_gate.py
normative: coverage_reporting.md
blocked_by: []
supersedes: []
---

# Current coverage reporting with preserved test outcomes

## What

The public main-branch badge inherited March coverage while recent complete
scientific executions did not upload their generated reports. The initial
maintainer decision deferred a forced suite; on 2026-10-01 the maintainer then
authorized one complete Linux/Python 3.13 execution to refresh the report.

## How

The existing weekly workflow gains an explicit manual single-interpreter option.
Its scheduled/default route retains the three-minor matrix and existing gates.
A pytest step retains the real exit status; only normal completed-suite statuses
0/1 allow artifact retention and main-branch coverage upload. Failed tests still
fail CI. Aborted/invalid suites cannot produce an accepted reporting claim.
See [the maintained procedure](../coverage_reporting.md).

## Why

Run 36868722733 on 2026-10-01 executed the full Python 3.13 suite: 4 failed,
10,298 passed, 2 skipped, 40 deselected, in 1,763.88 seconds. The preceding
scientific gate passed 54 cases. Upload was skipped solely because the package
tests failed. A coverage report and scientific pass are separate facts.

## What is measured and what is assumed

Native job/log inspection and downloaded XML establish both executions. The
authorized refresh completed and retained its report, with four test failures.
The native uploader succeeded, but independent Codecov processing remains
unconfirmed; no accepted service report or passing full matrix is claimed.

## What was refuted

Requiring a scientific pass before retaining/reporting coverage suppresses useful
measurement. Treating upload acceptance as test success would hide the failure.
Running all three Linux interpreters is unnecessary for the authorized single
report and cannot be confused with clearing full-matrix debt.

## Scope and exclusions

Reporting and explicit manual scope only. Existing scientific assertions, skips,
coverage exclusions, dependency sources and release rules retain their ownership.
No scientific repair or public package release is included.

## Acceptance criteria

One exact-source Linux/Python 3.13 full suite executes; actual results and XML
are retained; Codecov independently exposes a complete report for the uploader
SHA and numeric SVG; the README gains a scoped live badge. The matrix-debt guard
proves that one interpreter cannot pay full-suite debt; the maintained reporting
contract specifies failure and abort handling.

## Provenance

2026-10-01, host nauta for read-only preparation; prior hosted run
https://github.com/uibcdf/molsysmt/actions/runs/36868722733. The new hosted identity
and actual report/source observation are recorded below.


## Measured execution (recorded 2026-10-02)

[Run 36939842865](https://github.com/uibcdf/molsysmt/actions/runs/36939842865)
executed source `98e0d7832026df1f03320003d47ab9c4a6df2188` on Linux/Python
3.13 only. Native logs report pytest exit 1 after 2,338.79 seconds: 10,298 passed,
4 failed, 2 skipped, 40 deselected and 153 warnings. JUnit independently records
10,304 selected cases, 4 failures, 2 skips and no errors. The preceding scientific
truth gate passed 54 cases; that gate does not cancel the package-test failures.
The full test job and workflow correctly concluded `failure`.

The retained `full-suite-coverage-py3.13` artifact contains actual `coverage.xml`
and `junit.xml`, available from the run for 14 days. Parsing the Cobertura XML
with Python's standard `xml.etree.ElementTree` gives:

| Measure | Executed / measured | Coverage |
| --- | ---: | ---: |
| Python lines | 63,586 / 73,923 | 86.02% |
| Python branches | 15,152 / 21,240 | 71.34% |

There are 2,470 reported Python files. These are **coverage.py XML measures**,
not an accepted Codecov project percentage. The configured exclusions and
uninstrumented Rust execution remain as documented in the maintained procedure.
Counts below are obtained by grouping XML class filenames by their first path
segment and counting executable lines with nonzero hits; their totals were
checked against the XML root. Zero executable lines are not 100% coverage.

| Python area | Files | Executed / measured lines | Line coverage |
| --- | ---: | ---: | ---: |
| `form` | 1,665 | 41,105 / 47,401 | 86.72% |
| `_private` | 453 | 6,375 / 7,438 | 85.71% |
| `native` | 22 | 4,520 / 5,323 | 84.91% |
| `build` | 27 | 3,043 / 3,508 | 86.74% |
| `basic` | 37 | 2,130 / 2,459 | 86.62% |
| `structure` | 26 | 1,596 / 1,973 | 80.89% |
| `element` | 104 | 1,365 / 1,735 | 78.67% |
| `third_party` | 39 | 1,109 / 1,438 | 77.12% |
| `physchem` | 26 | 544 / 611 | 89.03% |
| `molecular_mechanics` | 8 | 317 / 436 | 72.71% |
| `interactions` | 9 | 307 / 326 | 94.17% |
| `pbc` | 14 | 281 / 309 | 90.94% |
| `topology` | 7 | 218 / 236 | 92.37% |
| `attribute` | 9 | 199 / 200 | 99.50% |
| `configure` | 3 | 188 / 196 | 95.92% |
| `(package root)` | 7 | 155 / 161 | 96.27% |
| `supported` | 7 | 127 / 151 | 84.11% |
| `core` | 1 | 5 / 12 | 41.67% |
| `hbonds` | 5 | 2 / 10 | 20.00% |
| `data` | 1 | 0 / 0 | No executable lines |


XML SHA-256:
`9615b46264936cd8c80d2618919ab53f666b1f217b2a9223eaba0affe7726f3d`.

### Actual failing contracts

| Selected test | Observed failure | Ownership |
| --- | --- | --- |
| `test_any_import_order_yields_the_shared_policy[molsysmt]` | `unified_atomic_mass_unit` differs from the expected `dalton` representation | Existing unit-policy adoption follow-up in uibcdf/molsysmt#244 and uibcdf/molsyssuite#18 |
| `test_any_import_order_yields_the_shared_policy[molsysviewer]` | Same representation mismatch in the reverse import order | Same existing unit-policy follow-up |
| `test_a_later_import_does_not_undo_the_user_choice` | Importing the pinned MolSysViewer changes the application's angstrom policy to nanometers | Same existing unit-policy follow-up |
| `test_the_converter_table_still_matches_the_converters` | The committed converter-argument table differs for `file:h5msm` | Component-owned converter contract; no repair included in this reporting task |

The unit-policy tests reside in `tests/cross_repo/test_unit_policy_authority.py`;
the table test resides in `tests/test_argument_contract.py`. The workflow's
controlled MolSysViewer source remains
`7a1522662e30575caf580a9447e3e6d80b628e07`; these results do not establish the
behavior of newer untested sibling sources. Assertions and scientific code were
not changed to obtain the report.

### Upload and independent processing evidence

Artifact retention succeeded at `2026-10-01T23:58:08Z`. The native Codecov upload
step succeeded at `2026-10-01T23:58:11Z`, with HTTP 200 after sending the report.
The source commit timestamp is `2026-10-01T23:15:38Z`, a separate fact.

At `2026-10-02T06:47:07.185353+00:00`, the central read-only probe
(`python devtools/scripts/coverage_audit.py --repository uibcdf/molsysmt`)
observed this exact source in the branch cache with null state/totals. The
independent commit endpoint likewise has no processed report, and the uploads
endpoint lists coverage as `started` with no totals; test-results ingestion is
separately `processed`. The public SVG has no numeric percentage. The newest
explicitly complete service report still observed belongs to March 24, not this
refresh. Successful transport is not acceptance.

The report is generated and retained; #286 remains partial specifically for
independent service acceptance and live-badge adoption. The README explains scope
and links the procedure while withholding the percentage badge. No second full
scientific execution or package publication is requested by this pending state.

## Guard relevance and verification

The ten tests in `devtools/tests/test_nightly_full_gate.py` pass. In particular,
`test_coverage_retention_preserves_failures_and_rejects_aborted_suites` exercises
the actual pytest exit-status wrapper and upload/retention conditions;
`test_only_an_explicit_manual_request_selects_the_single_coverage_lane` protects
the three-minor default, and
`test_single_python_coverage_cannot_clear_the_full_matrix_backlog` rejects debt
repayment by one successful interpreter. Hosted evidence independently confirms
only the requested interpreter ran and failed tests remained failed while XML
retention and transport succeeded. Service completion is deliberately not
inferred from those guards.


## Authorized transport replay (2026-10-02)

The maintainer authorized a replay and, if it still fails processing, adoption of
the independent automatic OIDC publisher strategy used by the three new suite
producers. Their jobs already follow their test jobs automatically; job separation
also permits publisher-only retries. The first MolSysMT replay preserves token
and flag, validates retained source provenance, and submits the unchanged XML for
source `98e0d7832026df1f03320003d47ab9c4a6df2188`. Its own documentation/workflow
commit is not the measured source. No scientific suite is rerun by this operation.
The replay run and observed service outcome will be recorded after execution.

The new local reusable artifact profile is contract-tested in
`devtools/tests/test_coverage_artifact.py`, including failed completed suites,
source identity, fork/branch/workflow rejection, aborted/missing/expired/ambiguous
artifacts, input safety and original-SHA publication. Existing ten suite/debt
guards continue to protect completed-suite retention and the full-matrix watermark.


### Token replay outcome and automatic OIDC adoption

[36979661341](https://github.com/uibcdf/molsysmt/actions/runs/36979661341)
completed successfully on publisher source `8a616e95f`. Native logs confirm the
original XML digest and measured source `98e0d7832026df1f03320003d47ab9c4a6df2188`.
The token upload ended at `2026-10-02T07:39:38Z`; at `07:43:41 UTC` the uploads
API still lists both coverage uploads as `started` without totals. No scientific
tests were run and no newly accepted service report is claimed by this replay.

As authorized, the weekly workflow now invokes an independent reusable OIDC
publisher automatically after the complete test job group, with the original run
ID. Completed failing suites remain reportable through successful artifact
retention; they remain failed. The routine test jobs do not receive OIDC write
permissions. Manual publication uses the same reusable workflow and existing
artifact, and preserves the original source SHA and XML timestamp. The component
coverage selections and `unittests` flag remain unchanged.

The nightly watermark now examines actual executed full-matrix jobs even if the
separate publisher failed. This prevents a coverage-service failure from forcing
an already successful scientific matrix to run again. All three successful
executed Linux minors are still required; scientific failures, aborted suites
and publisher-only runs cannot repay debt. The dedicated regression guard is
`test_publisher_failure_does_not_repeat_an_already_successful_full_matrix` in
`devtools/tests/test_nightly_full_gate.py`. OIDC hosted replay and independent
service acceptance will be recorded after execution.
