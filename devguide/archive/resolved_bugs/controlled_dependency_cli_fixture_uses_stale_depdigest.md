---
summary: Controlled-dependency CLI success fixture uses a DepDigest version below the public floor.
issue: uibcdf/molsysmt#429
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: low
verification: reproduced
area: [testing, dependencies]
guard: devtools/tests/test_validate_controlled_dependencies.py::test_cli_checks_the_real_runtime_contract_against_installed_versions
normative:
blocked_by: []
supersedes: []
---

# Controlled-dependency CLI success fixture uses a stale DepDigest version

**Reported:** 2026-10-22 while checking the source routes for
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.
**Status:** resolved test-fixture defect; runtime requirements remain unchanged.

## What

The CLI success case fails with a simulated DepDigest 0.11.0, while the public
requirement in `pyproject.toml` is already `depdigest>=0.15.1`:

```text
python -m pytest --receptor=llm devtools/tests/test_validate_controlled_dependencies.py -x
AssertionError: assert 1 == 0
```

## How

The test substitutes `importlib.metadata.version` with a fixed dictionary. Its
DepDigest value predates the public floor, so the real CLI correctly rejects
what the test mistakenly describes as a compliant environment.

## Why

The false negative obscures actual dependency-contract regressions and can
mislead a maintainer into changing an environment that already meets the floor.

## What was refuted

The actual development environment reports DepDigest 0.15.1+3.ga27172b, not the
fixture's 0.11.0. Neither upgrading the environment nor lowering the declared
runtime floor fixes this test defect.

## Resolution

Only the simulated DepDigest version changes to 0.15.1. The CLI, public
requirements and negative ArgDigest/transitive-requirement case are unchanged.
The named guard runs the actual CLI against the real project requirements and
checks both acceptance and rejection; it fails when the success fixture becomes
inconsistent with those requirements again.

## Provenance

Python 3.14 environment `molsyssuite@uibcdf_3.14`, source parent `c306ad50c`.
The prior documentation/controlled-dependency group ran all five selected cases:
four passed and this stale-fixture case failed. Focused corrected evidence is
recorded at closure. These tooling checks do not qualify a released addon or a
clean installed package pair.
