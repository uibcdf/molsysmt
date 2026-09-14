---
summary: Migrate legacy MolSysMT trees into the full Ruff gate.
issue: uibcdf/molsysmt#212
status: open
opened: 2026-09-12
closed:
verification: measured
area: [ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Migrate legacy MolSysMT trees into the Ruff gate

**Reported:** 2026-09-12, during the MolSysSuite policy rollout.
**Status:** Open; the critical-rule gate remains active during migration.

## What

Remove the temporary Ruff path exclusions for maintained MolSysMT code, tests and
documentation. The shared baseline currently checks maintenance tooling and the
MolSysViewer add-on, while the legacy core remains protected by the narrower
`F821,F822,F823,B006,B023` gate.

## How

Migrate one owned directory at a time. For each slice, run `ruff check --fix` and
`ruff format`, review all changes for semantic effects, run its scientific tests,
and remove its path exclusion only when lint and format checks pass. Keep the
critical core gate until the shared baseline covers the entire core.

## Why

An immediate full-tree migration is too large to review safely within the policy
rollout. On 2026-09-12, `ruff check molsysmt` found 13,500 violations with the
shared baseline. The legacy source and generated/form-adapter material need
separate, bounded review.

## What is measured and what is assumed

Measured: `ruff check --no-cache molsysmt` reports 13,500 violations under Ruff
0.16.5. `ruff check --no-cache --select F821,F822,F823,B006,B023 molsysmt`
passes. No claim is made that every violation needs a manual edit.

## What was refuted

An immediate all-tree formatter pass was rejected because it would mix extensive
style churn with the policy integration and weaken review of scientific behavior.
Simply excluding the core without a separate critical-rule gate was rejected
because that would remove an existing protection.

## Scope and exclusions

This proposal covers only the remaining Ruff migration. It does not change
scientific APIs or decide whether historical/generated files should ever be
formatted. Any permanent exclusion requires a separate justification.

## Acceptance criteria

- Every maintained Python tree passes the shared `E4,E7,E9,F,I` baseline and
  `ruff format --check` with no temporary path exclusion.
- Repository-specific Bugbear checks remain active where intended.
- Relevant scientific tests pass after each migrated slice.
- The central exception linked to this issue is removed.

## Dependencies and risks

The migration follows `uibcdf/molsysmt#211`. Import sorting or unused-import
fixes can affect registration side effects, so each slice needs behavioral review.

## Provenance

Local checkout, Python 3.13, Ruff 0.16.5, 2026-09-12 to 2026-09-14.
