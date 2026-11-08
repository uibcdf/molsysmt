---
summary: Rebudget the expanded native-plus-addon smoke after measured 25-minute exhaustion.
issue: uibcdf/molsysmt#611
status: resolved
opened: 2026-11-06
closed: 2026-11-08
verification: measured
area: [ci, molsysviewer]
guard:
normative: devguide/molsysviewer_addon.md
blocked_by: []
supersedes: []
---

# Expanded native-plus-addon smoke budget

## What

PR #543 proposes a finite 45-minute job maximum, preserving the complete native
and bound-addon test tiers and every scientific/performance assertion. This is
an operational ceiling, not a scientific runtime guarantee. The earlier #501
decision addressed 2,807 native / 1,845 addon cases and remains historical.

## How

Run 42210639321 on 9739f8dee1f8c71ae4e0043a19eb67acab8939ad is officially
cancelled. Check run 127868146225 explicitly annotates that the job exceeded
25m0s; job timestamps are 11:29:38–11:54:54 UTC on 2026-11-06. Native pytest
completed 6,042 passes, 23 optional skips, 642.10 s. The addon reached
3,760/4,699 before cancellation and has no terminal result. This run passed
the corrected distribution preflight; it is different from the earlier
missing-file inventory failure.

The owning script's complete paginated inventory contains 542 issues; #501 is
closed and no open continuation preceded this proposal. Sanitized public logs
and job metadata remain in `/tmp/msv-reader-distribution-smoke-42210639321*`.
The source receipt also retains the exact annotation and outcome. No complete
addon result is inferred from partial progress.

## Why / acceptance

The native tier takes roughly eleven minutes, the earlier clean complete addon
run took 1,072.21 s locally, and environment/build/cleanup also consume wall
time. A finite 45-minute ceiling covers that measured scope with runner
variability. Future splitting or optimization is separately measured; this
change removes no tests, assertions, provenance or required jobs.

The maintained contract is `devguide/molsysviewer_addon.md`. Keep the original
cancelled run and qualify official terminal success on the corrected source
before closing. Existing workflow/selection guards and actual hosted execution
are the checks; do not add a test merely mirroring the timeout literal. Owner
review/integration remains PR-only, and publication is not authorized.

## Corrected-source receiving

Smoke 42215709274 is officially successful on clean contribution 699fc69be
with the finite 45-minute maximum and both original tiers. The separate local
complete addon collection passes 4,699 cases without skips in 1090.15 s. The
original 25-minute cancellation remains non-success. Owner review/integration
of PR #543 is still required before this report is archived and closed.

## Owner decision and integration receiving — 2026-11-08

Accept the implemented finite 45-minute budget in `699fc69be`, retaining the
original cancelled 25-minute run. The corrected hosted source has official
terminal success (42215709274, attempt 1, 20m33s); its native 6,042 passes/23
skips and addon 4,695 passes/four skips remain their historical outcomes.
PR #543 is integrated. Current source retains all 105 prior native selectors
and, after separately received #653, all 74 addon modules in one invocation.
The unchanged completeness guard and external-reference module pass; clean
source `12a6c6fc2` receives all 104 selected developer/panel cases with no skips,
failures or errors. No guard, scientific assertion or budget limit is removed.

The [owner receipt](../../../devtools/data/smoke_budget_and_selection_receiving_611_653_20261108.json)
retains the complete original hosted capture, workflow comparison and later
selector failure/correction. This is source acceptance of the finite budget,
not a runtime guarantee or exact-current hosted success. The final candidate
still needs its own hosted and installed qualification. No workflow was
rerun and no package/release was authorized by this decision.
