---
summary: Rebudget the expanded native-plus-addon smoke after measured 25-minute exhaustion.
issue: uibcdf/molsysmt#611
status: partial
opened: 2026-11-06
closed:
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
