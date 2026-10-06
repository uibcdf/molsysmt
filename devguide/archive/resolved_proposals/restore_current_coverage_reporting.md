---
summary: Restore current Codecov evidence before reintroducing the coverage badge.
issue: uibcdf/molsysmt#286
status: resolved
opened: 2026-10-01
closed: 2026-10-06
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
See [the maintained procedure](../../coverage_reporting.md).

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

The eleven tests in `devtools/tests/test_nightly_full_gate.py` pass. In particular,
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
The replay outcomes below distinguish transport from service acceptance.

The new local reusable artifact profile is contract-tested in
`devtools/tests/test_coverage_artifact.py`, including failed completed suites,
source identity, fork/branch/workflow rejection, aborted/missing/expired/ambiguous
artifacts, input safety and original-SHA publication. Existing suite/debt
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
artifact, and preserves the original source SHA and XML timestamp. This first OIDC replay preserved the component coverage selections and
`unittests` flag; the later unflagged replay is recorded below.

The nightly watermark now examines actual executed full-matrix jobs even if the
separate publisher failed. This prevents a coverage-service failure from forcing
an already successful scientific matrix to run again. All three successful
executed Linux minors are still required; scientific failures, aborted suites
and publisher-only runs cannot repay debt. The dedicated regression guard is
`test_publisher_failure_does_not_repeat_an_already_successful_full_matrix` in
`devtools/tests/test_nightly_full_gate.py`. OIDC hosted replay is recorded below; independent service acceptance remains
pending.


### OIDC transport succeeded; service processing still pending

[36980687004](https://github.com/uibcdf/molsysmt/actions/runs/36980687004)
completed successfully for publisher source `3eb3bc82fb489c2e838059105fd00f93ac74de1d`.
It transmitted the same XML digest and original measured source using OIDC at
`2026-10-02T07:51:03Z`. At `2026-10-02T08:37:24.905483+00:00`, the independent
public API still has null report state/totals and all three coverage uploads
remain `started`; JUnit remains separately processed. OIDC therefore does not
establish a fix or service acceptance. No scientific execution was repeated.

The publisher now also matches the three new producers' unflagged whole-XML
submission. Current `.codecov.yml` removes the obsolete single-group carryforward
block to avoid inheriting March's group on future source reports. Existing Python
selection, coverage omissions, local thresholds and original XML/SHA remain
unchanged. The measured-source historical configuration is not rewritten. Any
processed report must still be inspected for sessions, scope and actual totals
before live-badge adoption. The controlled unflagged replay below tests this publication difference without
attributing the service failure to it beforehand.


### Unflagged replay and authenticated UI evidence

[36985514288](https://github.com/uibcdf/molsysmt/actions/runs/36985514288)
completed successfully on publisher source
`57050077465e1b385ea6b8efc10bc1fe01e559ad`, using OIDC and no upload flag.
Native logs confirm the unchanged XML digest and measured source. Transport
completed at `2026-10-02T08:42:33Z`; the independent probe at
`2026-10-02T08:44:45.489955+00:00` still found null totals and all four coverage
uploads in `started`.

The maintainer's authenticated Codecov commit page likewise shows `No Status`
and `Missing Head Report` for measured source `98e0d78`, with no report available
for comparison. This corroborates missing processing but supplies no processing
error or causal diagnosis. Token versus OIDC, job separation and removing the
flag have not resolved processing. XML validity, source mapping and public
repository activation have been checked; none proves backend acceptance.

A final bounded transport compatibility probe uses the pinned official action's
supported `use_legacy_upload_endpoint` input. The reusable publisher exposes it
as optional `legacy_upload`, default `false` for both triggers, so routine
automatic publication keeps the strategy used by the other producers. The
probe reuses the identical XML, source SHA and timestamp without executing tests.
Its native result and independent service state must be recorded separately.
All 33 local artifact/provenance and suite/debt tests pass; workflow lint, Ruff
and local developer-guide validation also pass.


### Legacy transport outcome and remaining diagnostic boundary

[36987144451](https://github.com/uibcdf/molsysmt/actions/runs/36987144451)
completed successfully on publisher source
`e28d37d143af50ee0e2d3513104a73c0cae91167`. Native logs show the official CLI
`--legacy` mode, original measured SHA and the same XML SHA-256. The upload
ended at `2026-10-02T08:59:48Z` with `Upload queued for processing complete`.
The independent check at `2026-10-02T09:03:55.181766+00:00` still has null
commit state/totals and no numeric SVG. The uploads listing contains the four
modern coverage requests in `started` and separately processed JUnit; no new
legacy entry is exposed in that listing. Native success therefore proves only
that the legacy request was queued, not a fifth processed or listed upload.

Routine publication remains automatic, independent and OIDC with the current
endpoint. No second scientific execution occurred in any replay. #286 remains
partial and the live badge remains withheld. Further identical retries do not
yet have a new diagnostic hypothesis. Provider-side processing logs or an
authenticated upload error are needed to distinguish the remaining causes;
the authenticated `Missing Head Report` notice does not do so.

The evidence above supplies a support packet: source run, original XML digest
and timestamp, exact measured versus publisher SHAs, four replay links,
authentication/flag/endpoint differences and separate service observations.
No signed storage URL, credential or account identifier is needed. Repository
activation, valid YAML, XML counts and tracked-source mapping were verified,
but none is a confirmed cause or a processing guarantee. There is no evidence
that changing scientific assertions, exclusions, the source SHA or report
timestamp would be a valid repair.

## Service acceptance and resolution — 2026-10-06

The maintainer reported provider recovery. The fresh read-only central probe at
`2026-10-06T05:55:17Z` independently observes a complete main report for
`a8f567c82c348bb003475e8b608721d1e51a9e07`, with 82.35% service coverage and a
numeric 82% SVG. No new scientific run or uploader replay was requested here.
The accepted report is a newer automatic execution, not the original October 1
artifact; no processing claim is made about the old replay attempts.

Native [run 37328009946](https://github.com/uibcdf/molsysmt/actions/runs/37328009946)
identifies that same source. Its Python 3.13 suite completed with 13,129 passed,
11 failed, 26 skipped and 40 deselected in 3,688.76 seconds. JUnit independently
records 13,166 selected tests, 11 failures, 26 skips and zero errors. The scientific
registry step passed 54 cases; it does not cancel the package failures. All three
Linux test jobs failed; artifact retention and the independent publisher passed.
The publisher used immutable artifact `11356906004` and the original source SHA.

Coverage XML SHA-256 is
`12f4f8914dd2285a5c838b3f71bb52bcf00f31db0c6e0934b79728efce8eeb2b`.
It contains 74,665/85,771 covered/valid lines and 19,483/26,210 covered/valid
branches. Codecov instead reports 68,560/83,249 hits/lines and 3,847 partials;
its processed percentage is not the XML line rate. Existing `.codecov.yml`
service ignores differ from `.coveragerc`; the observation does not isolate
all service normalization effects or claim numeric equivalence.
The [dated artifact](../../../devtools/data/stabilization_s5_20261006.json)
records native job outcomes, XML/JUnit identities, failing nodes and service totals.

The README's live badge is restored with explicit Python-source scope and a
warning that completed failures remain failures and later heads are unmeasured.
The matrix-debt and artifact provenance guards remain in place. S5 extends the
required Linux debt matrix to four Python minors and disambiguates the new weekly
macOS artifact names, while preserving the Linux/Python 3.13 publisher contract.
The 89 focused S5 checks pass. The executed full-suite failures remain for fresh
candidate triage under #237/#334; closing reporting does not clear test debt or
qualify a release. The durable contract is `devguide/coverage_reporting.md`.
