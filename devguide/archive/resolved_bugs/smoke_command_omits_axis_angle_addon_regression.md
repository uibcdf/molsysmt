---
summary: Smoke command omits the axis-angle addon regression module.
issue: uibcdf/molsysmt#639
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: medium
verification: reproduced
area: [ci, tests]
guard: devtools/tests/test_smoke_addon_test_command.py::test_all_addon_test_modules_are_arguments_of_one_pytest_invocation
normative:
blocked_by: []
supersedes: []
---

# Complete addon smoke arguments

## What

The explicit hosted addon pytest command omits the axis-angle expert-wrapper
regression module added with #602. The command-completeness preflight correctly
rejects it; source receiving must include all three mandatory preflights.

## How

Owner `b10160f29` combined with contribution `42f5ed3bc` on exact Viewer
`e4dd58cf0` produces 5,427 passes and one failure, with zero errors/skips. The
failure is the guard above: independent filesystem discovery contains
`tests/molsysviewer_molsysmt/test_axis_angle_rotation_tools.py`, absent from
the parsed single pytest invocation. The complete addon selection executes its
nine tests successfully. Original native exit one and result XML are retained.
This is an owner #602 integration omission, not a routing/scientific failure
introduced by the newer contribution. #611 retains its separate budget scope.

## Why

A new test must actually reach the hosted command. Passing local full-addon
execution or fourteen fast gates does not establish that source-lane coverage.
The guard protects real execution arguments rather than a comment or declaration.

## Correction and acceptance

Add the missing module argument to the existing invocation. Preserve the complete
native and addon tiers, the filesystem-derived expected set, the one-invocation
requirement and rejection of accidental shell commands. Do not remove discovery,
accept a partial list or invent passing hosted evidence.

Rerun all three preflights, the new wrapper module and complete combined-source
receiving. Retain the original failed campaign, published source identity and
consumer boundaries. No new method, dependency, progress weight, CI dispatch,
candidate or publication is selected. The new issue is admitted under #334 as
an included-regression delivery correction.

## Resolution — 2026-11-07

The existing smoke invocation includes the missing module. The unchanged
filesystem/parsed-command preflight and all other two preflights pass in the
complete owner receiving: **5,428 passed**, zero failures/errors/skips, native
zero. The original 5,427-pass/one-failure campaign is retained, not overwritten.
All selected source fingerprints match before/after both runs. The guard remains
addressable and continues to require every discovered module in one real command.
The [owner receipt](../../../devtools/data/bound_tools_newer_host_source_receiving_635_639_20261107.json)
keeps source identities, original failures and coverage scopes separate.
Source delivery/board verification follow in the release ledger. No hosted run,
budget change, new method or release approval is inferred.
