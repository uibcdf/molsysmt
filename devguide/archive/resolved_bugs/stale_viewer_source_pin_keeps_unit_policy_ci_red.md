---
summary: A stale MolSysViewer source pin keeps hosted unit-policy tests failing.
issue: uibcdf/molsysmt#293
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: high
verification: reproduced
area: [ci, deps, units]
guard: tests/cross_repo/test_unit_policy_authority.py
normative: devguide/dependency_contract_audit.md
blocked_by: []
supersedes: []
---

# A stale MolSysViewer source pin keeps hosted unit-policy tests failing

**Reported:** During formal closure review of uibcdf/molsysmt#185, 2026-10-02.
**Status:** Resolved with verified source, executable policy tests, and audited routes.

## What

Scheduled run 37008569379 reached the full suites for Python 3.11, 3.12,
and 3.13. Each reported three failures in shared-policy import order and
preserving a user angstrom policy, with 11,737 passes, 13 skips, and 40
deselections. The source pin predates the provider fix, although the
current public MolSysViewer release contains it. The earlier deferral in
release_1_0_status.md explained why this old pin remained; the maintainer's
current instruction to resolve reported bugs authorizes its correction.

## How

Routine smoke, weekly, benchmark, and docs routes and ci-full's default
fallback still used Viewer 7a1522662e30575caf580a9447e3e6d80b628e07.
They now use public 0.23.4 source cf427942d0b08a1c5c60f262c6a6b33f248d6f8b,
whose _pyunitwizard.py checks has_active_policy and declares the shared
standards. The dependency-contract inventory is updated in the same change.
Exact release-candidate SHA inputs remain explicit overrides.

## Why

The red suite hides new regressions and keeps the nightly backlog due.
Removing tests or forcing a user policy would conceal a real scientific
boundary violation. A verified source pin restores the intended boundary.

## What is measured and what is assumed

- GH Run Receptor confirmed the failed hosted run; bounded native failed-log
  inspection identified its actual pytest failures.
- The exact public tag resolves to the replacement SHA and its source
  initialization matches the corrected installed provider.
- A copy of the unmodified addressable policy test module passed all four
  applicable tests from the existing clean public MolSysMT 0.22.4 / Viewer
  0.23.4 Conda environment, Python 3.14.7, with the checkout excluded. This
  prefix lacks Pytest Receptor, so native pytest output and exit status were
  retained without modifying the clean installation.
- Local static route checks compare the manifest with every consumer and
  deliberately mutate a consumer pin to prove that disagreement fails.

## What was refuted

The hosted failure is not caused by missing CI triggers or the current public
Viewer artifact. It occurs because the workflow explicitly replaces that
provider with an older source revision. A recipe or public floor cannot
change an explicit source pin.

## Scope and exclusions

This updates the audited routine source and default candidate fallback.
It does not claim a new green hosted full matrix or new release certification.
Every 1.0 candidate still requires its exact paired source and package gates.

## Acceptance criteria

The controlled sources audit, its mutation tests, and the executable
`tests/cross_repo/test_unit_policy_authority.py` pass with the selected
corrected provider. The runtime guard runs inside hosted controlled
installations, where the old pin reproduces its scientific failure.

## Provenance

Hosted Linux, Python 3.11–3.13, run 37008569379, main 78981d6c1.
Local clean public Linux prefix: Python 3.14.7, MolSysMT 0.22.4 build 3,
Viewer 0.23.4 build 5. Source SHA verification used the public 0.23.4 tag;
2026-10-02.
