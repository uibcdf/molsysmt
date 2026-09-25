---
summary: Review inherited Python ecosystem policy in MolSysMT.
issue: uibcdf/molsysmt#244
status: partial
opened: 2026-09-25
closed:
verification: inspected
area: [ci, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in MolSysMT

**Reported:** 2026-09-25, from the MolSysSuite member rollout under
`uibcdf/molsyssuite#6`.
**Status:** Developer tools and support libraries are both partially reviewed.

## What

Review MolSysMT against the inherited MOLI Python support-library and
developer-tool policies. Track the two adoption states independently in the
MolSysSuite inventory.

## How

Pin published pytest-receptor 1.1.0 in the Conda test and development
environments. Use the `ci` profile in the standalone data-integrity workflow
and preserve its curated test selection. Retain the existing
`receptor_rerun_command` in `pytest.ini` for the repository's
`python -m pytest` invocation. The smoke, full, and weekly
workflows already select `--receptor=ci`; inspect hosted results with
gh-run-receptor and retain native GitHub checks when exact dependencies or
commands must be confirmed.

Review public API argument validation through ArgDigest, optional dependency
handling through DepDigest, diagnostic paths through SMonitor, and physical
quantity handling through PyUnitWizard. A declared runtime dependency is a
starting point, not proof that every applicable boundary is covered.

## Why

MolSysMT is a priority Python member in MolSysSuite. Before this review, the
test environment pinned receptor 0.6.0, the development environment omitted
it, and the standalone data-integrity workflow used plain pytest. Existing
main CI profiles already aligned with the MOLI rule but did not settle the
version pin or support-library applicability.

## What is measured and what is assumed

The initial discrepancy is inspected in `devtools/conda-envs/test_env.yaml`,
`development_env.yaml`, and `.github/workflows/ci-data-integrity.yaml` at
the source commit that opened this issue. Local receptor tests passed for the
curated provenance selector (one test) and the focused dependency and unit
policy selectors (nine tests). Ruff check and format, the dependency import
validator, and developer-guide validator passed. Hosted results will be added
after the exact implementation commit runs. No claim is made that the Python
3.14 transition in `uibcdf/molsysmt#237` is complete: the current MolSysSuite
repository checker reports the pre-existing `requires-python <3.14` and
missing Python 3.14 CI literals while this authorized transition is active.

## What was refuted

The existing `--receptor=ci` calls in smoke, full, and weekly CI do not imply
that every pytest workflow has the profile or that the declared plugin release
is current and reviewed.

## Scope and exclusions

This review does not alter scientific algorithms, public Python support
metadata, the MolSysViewer dependency, or the release gates of
`uibcdf/molsysmt#237`. It does not treat the backup workflow under
`.github/workflows/backups/` as an active CI gate.

## Acceptance criteria

- Every active hosted pytest command uses `--receptor=ci` with a declared
  published receptor release; local agent tests use `--receptor=llm`.
- The exact source commit passes applicable local checks and hosted gates,
  or the remaining failures are identified and linked without weakening tests.
- The member issue and MolSysSuite inventory record applicable support-library
  boundaries, evidence, and any bounded remaining work.

## Dependencies and risks

`uibcdf/molsysmt#237` separately owns the Python 3.14 transition. Its active
CI and packaging work can affect broad hosted gates, so receptor adoption
must be judged on its own evidence as well as the full workflow conclusion.

## Support-library applicability checkpoint

All four inherited boundaries are present in MolSysMT. Public argument
digesters live in `molsysmt/_argdigest.py` and the private digester modules;
optional backend declarations and checks live in `molsysmt/_depdigest.py` and
form adapters; coded diagnostics live in `molsysmt/_smonitor.py` and the
SMonitor integration; unit policy and quantity conversion use
`molsysmt/_pyunitwizard.py` and PyUnitWizard at public physical-quantity
boundaries. The runtime metadata declares all four libraries. Local focused
receptor tests passed 82 cases across quantity digesters, SMonitor contracts,
and diagnostic exceptions, in addition to the nine dependency and unit-policy
cases above.

This is a `partial` support-library review. Existing targeted tests show active
integration, but `uibcdf/molsysmt#155` still tracks the PyUnitWizard fast-path
audit, and `uibcdf/molsysmt#236` tracks warning reconstruction against SMonitor
0.16. The Python 3.14 published-installation claim belongs to
`uibcdf/molsysmt#237`. These open boundaries need explicit decisions or tests
before calling the member review adopted; the dependency list alone is not
enough.

## Hosted checkpoint for source commit de9e9c9

The [bundled data integrity run](https://github.com/uibcdf/molsysmt/actions/runs/36105299656)
passed. Its native log confirms published PyPI `pytest-receptor==1.1.0` and
the curated `--receptor=ci` command, with one test passed. The
[developer-guide run](https://github.com/uibcdf/molsysmt/actions/runs/36105299549)
passed. GH Run Receptor inspected both. The smoke run `36105275404` was
cancelled during the test step, so it supplies no successful test conclusion.
The [weekly run](https://github.com/uibcdf/molsysmt/actions/runs/36105275495)
failed in all three Python cells, and the
[six-cell full matrix](https://github.com/uibcdf/molsysmt/actions/runs/36105299602)
failed in all six cells. Each failing job reached its full pytest step.
The Python 3.12 Ubuntu matrix log confirms `pytest-receptor 1.1.0 py_1` from
`uibcdf` and a native pytest exit status of 1, preserved in receptor's
`FAIL exit=1` report. In both workflows, three assertions in
`tests/cross_repo/test_unit_policy_authority.py` fail: import order does not
produce one shared unit policy, and importing MolSysViewer resets a user's
chosen unit. The receptor did not report a rendering error. The same full
matrix passed on separate source revision `8d58581` with newer controlled
SMonitor, ArgDigest, and MolSysViewer revisions; this comparison suggests an
outdated controlled source set at `de9e9c9`, but does not isolate one
package as the sole cause. This member review keeps developer tools `partial`
until the ordinary test gate passes on the exact integrated revision. The
controlled-source update also had to coordinate with the Python 3.14 transition in
`uibcdf/molsysmt#237` and `uibcdf/molsyssuite#29`.

## Later main integration

After the failed `de9e9c9` runs, MolSysMT merged candidate `89ceda0ad` into
`main`. This merge contains the later controlled source revisions and the
authorized Python 3.14 metadata; the earlier failing runs remain evidence
about `de9e9c9`, not a conclusion about the merged `main`. On the merged
checkout, the MolSysSuite repository checker passed, and the focused
`tests/cross_repo/test_unit_policy_authority.py` selector passed six tests
locally with `--receptor=llm`. The developer-guide validator and Ruff check
also passed. The earlier candidate `e28ceb9ea` passed the six-cell full
matrix in run `36120923064` with controlled MolSysViewer commit
`cf427942d0b08a1c5c60f262c6a6b33f248d6f8b`, but that branch had not yet
merged this review's receptor 1.1.0 pins. The merged `main` advanced to
`6a334cc3e` with a Conda validation change. Its exact-commit full matrix was
dispatched as run `36132035176` using the same controlled Viewer commit. In
its first attempt, the macOS/Python 3.11 cell stopped while building the
editable MolSysMT package: rustup reported that `rustc` was absent from the
runner's `1.97.1-aarch64-apple-darwin` toolchain. That cell did not reach
pytest, so it provides no evidence about the receptor or the unit policy.
The other five test cells were still running at this checkpoint. The
developer-tools review remains `partial` until an integrated full gate passes.
