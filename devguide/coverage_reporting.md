# Coverage reporting

`ci-weekly.yaml` runs the existing complete suite (including configured doctests)
under pytest-cov using the maintained `.coveragerc`. It measures Python source
for `molsysmt` with the existing declared exclusions; it does not instrument Rust
execution or silently change the denominator. Linux/Python 3.13 uploads to Codecov.
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
the selected main-branch uploader may publish coverage. Failed tests keep the job
and workflow failed. Collection errors, interruption, internal errors or no tests
(exit 2–5) do not publish coverage. Missing XML or service errors fail the upload.
There is no `continue-on-error` and no common percentage floor.

The action pins official Codecov v7.1.1 with signature checks enabled and uploads
only the specified XML. Independent service inspection must match a complete
report and numeric live SVG to the actual uploader's source SHA before restoring
the README badge. The percentage describes the last uploaded report and can lag
later lightweight/skip pushes; it is not a statement that all tests passed.

Scientific failures are routed to the component's existing owning issues and team.
The reporting repair is uibcdf/molsysmt#286, coordinated by uibcdf/molsyssuite#69.
