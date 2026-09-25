---
summary: Review inherited Python ecosystem policy in MolSysMT.
issue: uibcdf/molsysmt#244
status: active
opened: 2026-09-25
closed:
verification: inspected
area: [ci, deps, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in MolSysMT

**Reported:** 2026-09-25, from the MolSysSuite member rollout under
`uibcdf/molsyssuite#6`.
**Status:** The developer-tool adoption is being validated; support-library
applicability remains under review.

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
