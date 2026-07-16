# Proposal: Independent Ruff CI Workflow

**Status:** partially superseded; revalidation required
**Owner:** MolSysMT  
**Related precedent:** TopoMT `.github/workflows/ruff.yaml`

## Purpose

MolSysMT declares Ruff as a development dependency, but no active GitHub Actions
workflow runs it. The smoke and full CI workflows currently execute tests only.
This means lint regressions can enter `main` even though Ruff is available to
developers.

> **Revalidated 2026-07-13:** `pyproject.toml` now contains canonical
> `[tool.ruff]` and `[tool.ruff.lint]` sections with a limited correctness rule
> set. The remaining proposal is the independent CI workflow and any deliberate
> expansion of those rules. The original current-state bullets below are kept
> only to explain the proposal's origin.

## Current State

- `pyproject.toml` declares Ruff, Black, and isort in the `dev` extra.
- A canonical, limited `[tool.ruff]` configuration is now present.
- No workflow, pre-commit hook, Makefile target, or development script executes
  `ruff check` or `ruff format --check`.
- Existing CI should remain focused on test matrices; linting does not need to be
  repeated for every OS and Python version.

## Proposed Change

Add a dedicated `.github/workflows/ruff.yaml` workflow with one Ubuntu job.
Before enabling it, define a minimal canonical Ruff configuration in
`pyproject.toml` and make the selected rules pass locally.

The first enforced rule set should contain only correctness-oriented checks with
low ambiguity:

```bash
ruff check molsysmt --select F821,F822,F823,F841,B006,B023
```

The workflow should:

- run on pull requests and pushes to `main` affecting Python source,
  `pyproject.toml`, or the workflow itself;
- support `workflow_dispatch`;
- use a bounded Ruff version range;
- run independently from test matrices;
- avoid enforcing formatting or broad style rules in the first phase.

## Staged Adoption

1. Revalidate and, if necessary, adjust the existing `[tool.ruff]` and
   `[tool.ruff.lint]` rules.
2. Correct all violations reported by the initial command.
3. Add the independent workflow and require it on pull requests.
4. Evaluate broader lint and formatting enforcement separately.
5. Once Ruff replaces their responsibilities, evaluate removal of Black and
   isort declarations in a separate cleanup.

## Acceptance Criteria

- The documented local Ruff command passes from a clean checkout.
- The independent workflow passes on `main` and fails on an introduced critical
  lint violation.
- Linting runs once per relevant revision, not across the full test matrix.
- Existing smoke, full, and weekly test workflows remain unchanged.

## Non-Goals

- Enforcing repository-wide formatting immediately.
- Removing Black or isort without a separate compatibility review.
- Treating existing style debt as blocking before the critical rules are clean.
