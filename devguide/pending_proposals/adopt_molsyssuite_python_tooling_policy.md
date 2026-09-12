---
summary: Adopt the shared Python and Ruff development baseline.
issue: uibcdf/molsysmt#211
status: active
opened: 2026-09-12
closed:
verification: measured
area: [ci, maintenance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Adopt the MolSysSuite Python tooling policy

## What

Align MolSysMT with the Python-library contract governed by
`uibcdf/molsyssuite#6`: Ruff as formatter, import sorter, and linter with the common
`E4`, `E7`, `E9`, `F`, and `I` baseline. Its Python
`>=3.11,<3.14` support range and 3.11–3.13 CI matrix already match the suite.

## How

Extend the existing repository-local Ruff selection, pin the suite-tested Ruff release
in the development environment, remove Black and standalone isort from active
development dependencies, and invoke the reusable MolSysSuite conformance workflow.
Preserve MolSysMT-specific Bugbear rules and its broader scientific validation gates.

## Why

MolSysMT is one of the six wave-1 libraries being stabilized first and a major consumer
of the other core tools. One quality gate reduces cross-repository maintenance without
flattening its domain-specific tests or documentation lifecycle.

## Evidence

The policy 1.0 checker on 2026-09-12 reported `RUFF_CONFIG`, `RUFF_CI`, and active
Black and isort dependencies. Existing workflows run Ruff linting but do not enforce the
shared import baseline and formatting check.

## Acceptance criteria

- The central conformance checker reports no findings.
- Ruff lint and format checks pass with the suite-tested release.
- The relevant MolSysMT validation suite passes.
- The local issue and this record close together after the guard is published.

