# Coverage reporting

`ci-weekly.yaml` runs the existing complete suite (including configured doctests)
under pytest-cov using the maintained `.coveragerc`. It measures Python source
for `molsysmt` with the existing declared exclusions; it does not instrument Rust
execution or silently change the denominator. Its retained Linux/Python 3.13 XML
is published by an independent OIDC job.
The normal weekly/nightly Linux matrix retains Python 3.11, 3.12 and 3.13.

For an explicitly authorized single coverage refresh:

```bash
gh workflow run ci-weekly.yaml -R uibcdf/molsysmt --ref main \
  -f python_313_only=true -f probe_backlog=false
```

The boolean selection applies only to manual dispatch. It reuses the existing
setup, controlled dependency validation and scientific gates; scheduled/default
runs keep the full matrix. A single interpreter cannot clear the skipped-commit
backlog, which requires successful executed suites on all three Linux minors.
It also does not qualify a release or establish support for untested platforms.

The pytest step preserves its actual exit code. After exit 0 (passed) or exit 1
(completed with test failures), XML and JUnit results are retained for 14 days and
the independent main-branch uploader may publish coverage. Failed tests keep the job
and workflow failed. Collection errors, interruption, internal errors or no tests
(exit 2–5) do not publish coverage. Missing XML or service errors fail the upload.
There is no `continue-on-error` and no common percentage floor.

After the full matrix completes, `coverage-upload` automatically calls the
reusable `ci-coverage-upload.yaml` publisher using this run ID. No manual action
is needed for eligible weekly, conditional-nightly or full manual runs. The
test jobs have read-only permissions; only the publisher receives `id-token:
write` and authenticates with OIDC. Test failures remain visible. Aborted or
missing producer artifacts fail provenance validation and cannot publish.
A successful executed three-minor matrix pays test debt even if the separate
publisher fails; a failed scientific matrix or publisher-only replay cannot.

The action pins official Codecov v7.1.1 with signature checks enabled and uploads
only the specified XML. Independent service inspection must match a complete
report and numeric live SVG to the actual uploader's source SHA before restoring
the README badge. The percentage describes the last uploaded report and can lag
later lightweight/skip pushes; it is not a statement that all tests passed.

Scientific failures are routed to the component's existing owning issues and team.
The reporting repair is uibcdf/molsysmt#286, coordinated by uibcdf/molsyssuite#69.


## Latest measured execution

The explicitly authorized [2026-10-01 execution](https://github.com/uibcdf/molsysmt/actions/runs/36939842865)
retained full Linux/Python 3.13 XML. The [owning report](pending_proposals/restore_current_coverage_reporting.md#measured-execution-recorded-2026-10-02)
records line/branch measures, area breakdown, actual test failures and successful
transport separately from pending Codecov processing. Until the independent
service exposes a complete report for the tested SHA, the live README badge
remains withheld under uibcdf/molsysmt#286.


## Replaying a retained report

`ci-coverage-upload.yaml` republishes an existing full-Linux Python 3.13 artifact
without installing MolSysMT or executing tests:

```bash
gh workflow run ci-coverage-upload.yaml -R uibcdf/molsysmt --ref main \
  -f source_run_id=36939842865
```

The local reusable profile `select_source(run_id, fetch=...)` in
`devtools/scripts/coverage_artifact.py` checks native run, producer-job and
artifact metadata. It accepts only the owning `main` weekly workflow, a completed
Python 3.13 suite and successful report retention, and a unique unexpired artifact
whose run/repository/branch/SHA match. Missing, ambiguous, aborted, forked or
unavailable evidence fails publication. It emits safe run/SHA/artifact IDs;
GitHub's existing API client and artifact action perform authenticated reads.
`inspect_xml(path)` checks nonempty Cobertura counts and records the XML digest.
Neither operation executes artifact contents or changes coverage selections.

The uploader checks out the measured source for path mapping and explicitly
submits its original commit SHA and branch, rather than relabelling old coverage
as the publisher's commit. The downloaded XML stays outside the checkout so the
source switch cannot delete it. The first controlled replay retained the existing
token and `unittests` flag but remained unprocessed. The reusable publisher now
uses OIDC, automatically after the full test job group or through this explicit
manual replay. Like the three new suite producers it sends the specified complete
XML without a flag. The obsolete single `unittests` carry-forward declaration
is removed from current configuration so future reports do not silently inherit
that historic group; Python selections, exclusions and local thresholds remain. Test debt follows actual matrix success independently of transport.
Independent service processing is still required after successful transport.

Artifact retention is 14 days; it does not override Codecov's default 12-hour
report-age check. A replay preserves the original XML timestamp. See the
[official age setting](https://docs.codecov.com/docs/codecov-yaml#expired-reports)
when an explicitly reviewed older report needs a separately bounded service
configuration; do not regenerate timestamps to imply a fresh execution.
