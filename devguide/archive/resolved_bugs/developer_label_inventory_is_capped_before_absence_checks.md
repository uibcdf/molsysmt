---
summary: Developer label inventory is capped before absence checks
issue: uibcdf/molsysmt#724
status: resolved
opened: 2026-11-12
closed: 2026-11-12
severity: medium
verification: reproduced
area: [docs, tests]
guard: devtools/tests/test_devguide_issue_pagination.py::test_label_absence_is_decided_after_every_label_page
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


## Resolution — 2026-11-12

Implementation 9af9be18c receives every native REST page before deciding label
absence. The primary regression checks the actual missing-label decision on
201 valid records: the existing last label survives and only the truly absent
name is returned. An additional assertion rejects replacing 200 with a larger
finite cap. Shape/transport failures remain errors; open/sync semantics and
#159's partial application are retained.

The final 75-case cohort passes after the guard refinement; it peaks near
137 MiB within one CPU/1.5 GiB/no own swap and preserves at least 14.25 GiB
host available memory. The live read-only probe receives 72 labels, recognizes
an existing requested name and reports only a known-absent sentinel. It does
not claim that the live board exceeds 200 or perform label writes.

The [receiving receipt](../../../devtools/data/developer_label_inventory_receiving_724_20261112.json)
owns exact tested input hashes, source/delta attribution, all failed and
resource-deferred attempts and scopes. Local contributor/reporting guidance
now applies full acquisition to both issues and labels. Central MolSysSuite
#171/MolI #85 adoption remains separately owned.
