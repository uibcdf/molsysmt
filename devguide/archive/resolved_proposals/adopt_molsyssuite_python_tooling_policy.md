---
summary: Adopt the shared Python and Ruff development baseline.
issue: uibcdf/molsysmt#211
status: resolved
opened: 2026-09-12
closed: 2026-09-19
verification: measured
area: [ci]
guard: devtools/tests/test_ruff_clean.py
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

## Staged outcome — 2026-09-14

The central conformance checker and the configured repository-wide Ruff checks now
pass. Ruff 0.16.5 is pinned, the shared workflow is installed, and Black/isort are
removed from active development tooling. The legacy core, tests and documentation
remain temporarily excluded from the full baseline. A separate critical-rule gate
continues to scan the core; `uibcdf/molsysmt#212` owns removal of the exclusions.

This is adoption with a tracked exception, not a claim that the entire source tree
has been reformatted. The four MolSysMT–MolSysViewer add-on integration failures
observed in this checkout concern a missing `visible_atom_indices` attribute and
are not accepted as a consequence of this tooling migration; they remain outside
this report's acceptance decision.

## Acceptance criteria

- The central conformance checker reports no findings.
- Ruff lint and format checks pass with the suite-tested release on the declared
  boundary, and the separate critical-rule core gate passes.
- The relevant MolSysMT validation suite passes.
- The remaining exclusions have their own issue and central exception record.
- The local issue and this record close together after the guards are published.

## Resolution

MolSysMT adopts policy 1.1.6 with Ruff 0.16.5, the common configuration and
workflow, and no active Black or standalone isort dependency. The maintenance
suite passed with 157 tests and policy run `35468885292` passed. The deliberate
legacy-tree boundary remains a central exception owned by `uibcdf/molsysmt#212`;
the critical-rule core test stays active until that issue removes the exclusions.
