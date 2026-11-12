---
summary: Developer label inventory is capped before absence checks
issue: uibcdf/molsysmt#724
status: active
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [docs, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Acquiring all repository labels before declaring absence

## What

The developer issue tool reads at most 200 labels, then treats its set as a
complete inventory. A valid label after that cap is incorrectly declared absent.
The reporter observes 72 labels on the live board: this is a reproduced larger
transport defect, not a current claim that the board exceeds the limit.

## How

Owner source confirms `_board_labels` uses `gh label list --limit 200`.
Substitute only the native transport with 201 valid label records and put the
requested existing label last. Retain the source logic and check the actual
missing-label decision. Receive complete REST pages through the same native
pagination pattern as the completed issue-inventory route, validating page and
record shape before interpreting absence. Malformed/failed acquisition must
remain an error rather than an empty label set.

## Why

False absence can refuse a valid issue-opening request or prevent correct
state/area synchronization. Raising the cap only postpones the defect. Preserve
the existing distinction between truly absent labels and unavailable evidence,
and retain #159's partial label application plus #587's issue pagination.

## Scope and acceptance

Guard the beyond-cap decision, legitimate empty pages, malformed/failed input
and existing open/sync behavior. No automatic label creation, renaming, report
deletion, scientific/runtime change, dependency floor or release action belongs
to this correction. Shared acquisition governance remains MolSysSuite #171;
this owner fixes its local route without claiming wider adoption.

## Provenance

2026-11-12 intake from the central team's report. The unchanged function is
inspected locally; controlled before/after transport receiving follows. The
original live-label count and source evidence remain in the owning issue.


## Owner source receiving

The controlled baseline has ten failures and six passing controls. One failure
is the reproduced real absence decision on a valid 201-label old transport.
The other nine specify empty/malformed REST/JSON transport behavior for the
new route; they are not nine additional old CLI incidents. Full acquisition
now uses native gh api --paginate --slurp, validates page/name shape, and
keeps malformed/failed acquisition as an error. The affected label/issue
pagination, open/sync, workflow and devguide-validator cohort passes 75 cases.

The first correction attempt is deferred before pytest by the shared-host
admission rule (native wrapper status 75). A separate Ruff preparation stop
and the initially incorrect attribution of that deferral are retained with
a corrected disposition; the actual admission record controls the result.
The next bounded corrected2 run passes, using one CPU/1.5 GiB/no own swap,
with about 205 MiB peak and no resource stop. Scientific/runtime behavior,
issue creation policy and label mutation semantics are unchanged.
