---
summary: Hosted addon smoke omits newly integrated regression modules.
issue: uibcdf/molsysmt#701
status: active
opened: 2026-11-10
closed:
severity: medium
verification: inspected
area: [ci, tests]
guard: devtools/tests/test_smoke_addon_test_command.py::test_all_addon_test_modules_are_arguments_of_one_pytest_invocation
normative:
blocked_by: []
supersedes: []
---

# Hosted addon smoke omits new regression modules

## What / How / Why

Public 5f241cfa7 contains the assessed-protonation and secondary-structure
modules, but its single hosted addon pytest command does not select them.
The existing complete-inventory guard reports the mismatch. PR #702 supplies
both selectors and its new figure-observation module without changing that
guard or removing any previous selection.

Owner integration also adds the new bounded Jupyter stage-diagnostic module
to the same command. All addon test modules must remain arguments of one
actual pytest invocation; a path mentioned in a comment is insufficient.
This changes hosted coverage, not a scientific calculation or CI dispatch.

## Acceptance

Receive the unchanged exact-inventory guard, workflow/dependency source-route
controls and the full affected addon cohort against the explicitly selected
Viewer source. Preserve the incoming failed 41-pass/one-failure attempt in the
author receipt. A local passing command does not certify a hosted run,
installed pair or release candidate.
