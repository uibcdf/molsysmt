---
summary: Devguide board reconciliation falsely loses issues older than its capped inventory.
issue: uibcdf/molsysmt#587
status: partial
opened: 2026-11-05
closed:
severity: medium
verification: reproduced
area: [docs]
guard: devtools/tests/test_devguide_issue_pagination.py::test_remote_state_keeps_old_issues_beyond_five_pages_and_filters_prs
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Complete issue acquisition before board reconciliation

## What

The board script uses `gh issue list --limit 500`, then interprets missing
entries as nonexistent issues. Valid old #22 and #25 are incorrectly rejected.

## How

Reproduced on source 8c2661293 and the receiving contribution. Direct independent
GitHub queries find #22 closed and #25 open with the expected titles. The
original script cannot see either outside its latest-500 result. The transport
regression supplies five full pages and a later page with both old identities
and a PR control; it fails the old limited command before the correction.

## Why

Compact presentation is separate from complete acquisition. An audit must
distinguish confirmed absence from truncated/failed acquisition. Raising the
constant, deleting valid local records or suppressing drift only conceals the
failure. No wider component prevalence is asserted. Cross-component review is
tracked in uibcdf/molsyssuite#171 and uibcdf/moli#85 at Diego's request.

## Proposed fix and verification

PR #543 replaces the capped query with repository-context REST pagination and
normalizes the existing title/state/label schema. PR entries are excluded.
Valid empty JSON inventories remain empty; an empty body or acquisition failure
cannot become a successful missing-issue result. The local working instruction
and reporting contract preserve these distinctions. Tests and live acquisition
keep real label/status drift visible rather than hiding it.

Scientific/addon runtime remains unchanged from the separately qualified
8725a460c source. This is a tooling follow-up with its own guard and receipt;
it does not relabel the prior 4,506-case gate as a new full execution. Owner
review/integration remains pending, so the report stays partial until accepted.
