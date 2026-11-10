---
summary: Hosted addon smoke omits newly integrated regression modules.
issue: uibcdf/molsysmt#701
status: resolved
opened: 2026-11-10
closed: 2026-11-10
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

## Resolution — 2026-11-10

Owner source **d36d25929** receives exact PR **#702 9dff314f8** and includes
all new modules in the same hosted invocation. **5,959 addon/caller/source-route
cases pass without skips**, including the unchanged complete-inventory guard.
Fifteen fast gates pass. The [owner receiving record](../../../devtools/data/figure_context_owner_receiving_701_702_615_20261110.json)
retains the author's original missing-selector failure and the distinct owner
browser setup failure; no existing selector, assertion or deadline was removed.
This resolves command coverage, not execution of a hosted or installed matrix.
The exact Viewer source is 5164f13bb503625dbe65f3b657ab5260feadcb65; scientific
profiles, installed qualification and publication authority remain separate.
