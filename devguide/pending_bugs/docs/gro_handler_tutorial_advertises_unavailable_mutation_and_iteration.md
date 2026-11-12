---
summary: GRO handler tutorial advertises unavailable mutation and iteration
issue: uibcdf/molsysmt#716
status: active
opened: 2026-11-11
closed:
severity: medium
verification: reproduced
area: [docs, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reconciling the GRO handler tutorial with actual operations

## What

The tutorial implemented-operations table claims partial extraction, addition,
merging, structure appends, setters and streaming iteration. The adapter only
supports complete resident copies/extraction; mutation hooks reject, its setter
module has no delivery routes and both iterator classes reject iteration. A
later paragraph correctly limits extraction, contradicting the table.

## How

Inspect the six-cell GROFileHandler tutorial against the actual form adapter.
Its 62 attribute declarations and five conversion registrations are real, but
not proof that every stored GRO entry contains every quantity. Foundations
already explains the resident first-entry scope, inference and provider limits.
Its copy example closes normally but creates the copy outside the protected
scope, and does not demonstrate selected public quantities.

## Why

Users can select unsupported operations from a table labelled implemented.
A reader should distinguish registered names, real operations, source fields
and derived attributes without relying on an unsuccessful call to learn the
scope. Preserve the existing reader and honest unsupported outcomes.

## Scope and verification

Correct tutorial prose and paired instructions, retaining six cells, anchors,
62 attribute declarations and five conversion references. Keep stored code,
outputs and execution metadata unchanged when only Markdown changes. Improve
and execute the actual Foundations example under nm/ps and pm/fs with deposited
coordinate fields as the independent oracle and deterministic buffer cleanup.

Use a small literal three-atom GRO entry to execute documented operation limits,
including nonmutation after refusal and independent complete-copy ownership.
The primary guard checks actual behavior against table availability. It does
not certify all natural-language descriptions or the full external format.
Existing GRO bridge/provider and conversion-truth contracts remain applicable.
No runtime/native implementation, dependency, scientific model, writer or
streaming feature is introduced. Support-library boundaries remain unchanged;
no new third-party method needs Ackredit registration.

## Acceptance

- The table distinguishes whole-handler extraction, real copying, piped reads
  and unavailable mutation/iteration, with no contradicting claims.
- Actual operation outcomes and selected public coordinates agree with the
  corrected documentation, under both unit policies, without changing sources.
- The 62 declarations, five conversion references and notebook execution payload
  survive; actual generated articles and their targets/anchors are inspected.
- Focused tests, relevant lint/governance and strict HTML pass with bounded
  shared-host resource use. Retain original failures and setup attempts.

## Provenance

2026-11-11, Linux/Python 3.14 development source. Initial read-only inspection;
execution uses the already reviewed pinned client/support overlays and unchanged
qualified native binary. No final source/installed/candidate acceptance follows.

## Bounded source receiving

The original six-route documentation check fails all six cases: five reach the
wrong availability assertions; the iterator hits the separate constructor defect
now tracked by #717. Preserve that baseline rather than calling all six pure
text failures. #717's 103-route baseline reproduces the same TypeError at every
reviewed refusal branch. Both corrections share a later 166-case passing cohort:
103 diagnostics, eight documentation/example cases, four GRO record contracts,
34 GRO bridge/copy/refusal cases and 17 public iterator controls. No skips occur.
The actual Foundations example executes under nm/ps and pm/fs with fixed-column
source coordinates as the independent oracle, closes both buffers, preserves
independent arrays and leaves the 5,547-atom input bytes unchanged.

The tutorial's six cells, code/outputs/execution metadata, 62 declarations and
five conversion references are preserved. Only its explanatory Markdown changes;
no new execution mark is claimed. A source-only review of course notebooks
checks for this form/diagnostic without running or modifying their examples.
The 15 fast release gates and applicable Ruff/index checks pass. Complete HTML
and actual generated article/reference receiving remain pending before closure.
The first edit helper stopped on a duplicated short manifest key; selecting the
unique page-path context completed that update. No partial script is treated as
proof of finished edits.
