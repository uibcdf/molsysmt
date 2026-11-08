---
summary: Bound addon smoke omits the external-reference panel regression module
issue: uibcdf/molsysmt#653
status: active
opened: 2026-11-08
closed:
severity: medium
verification: reproduced
area: [ci, tests]
guard: devtools/tests/test_smoke_addon_test_command.py::test_all_addon_test_modules_are_arguments_of_one_pytest_invocation
normative:
blocked_by: []
supersedes: []
---

# Missing external-reference smoke argument

## What

On unchanged smoke workflow `03c59caef9`, the existing complete-addon selection
control fails because `test_external_reference_panel.py` is absent from the
single pytest invocation. The directed developer receiving records 59 passes
and this one failure. The guard is correct; this is not a benchmark-data or
molecular fitting failure.

```bash
python -m pytest --receptor=llm devtools/tests/test_smoke_addon_test_command.py
```

## How and why

The external-reference regression module was introduced after the earlier
#639 argument repair, but the smoke's explicit file list was not extended.
The dynamic guard compares actual arguments against every current addon test
module and rejects the omission before hosted scientific execution. Add the
missing file to that same invocation; do not relax the guard, remove the
module, narrow pytest selection or add an independent shell command.

## Acceptance and scope

The unchanged guard and the external-reference module must execute successfully;
retain the original failure and verify that all current addon modules are
selected exactly once in one invocation. The default full CPU source suite
already executes this module successfully as part of its 32,039 selected
cases, but does not by itself repair the separate CI command. No molecular
algorithm, geometric assertion, provider pin, timeout or benchmark threshold
changes. Final-candidate hosted execution remains independently required.

## Provenance

Measured 2026-11-08 in the existing Linux/Python 3.14.7 development environment,
with recorded Viewer `e4dd58cf0edcb2c3afb2c982ccd50d3899d504ab` and native binary
unchanged. The private directed receipt and original failed JUnit are retained
under the owning source receiving. #611 retains the finite-budget decision;
this report owns only the new missing selector.

## Directed receiving — 2026-11-08

The unchanged selector guard and all 44 external-reference cases pass together:
45 passes, zero skips/failures/errors, native exit 0. Every current addon module
is now an argument of the one existing pytest invocation. The 44 legacy-H5MSM
warnings remain visible. Peak process-tree memory is 596,873,216 bytes under
the one-CPU/two-GiB cap, with no memory or task-limit events. This working-tree
receiving preserves the original one-failure/59-pass report and changes no
molecular code or assertion. Publication/board closure follows the clean-source
checkpoint; final candidate hosted gates remain separate.
