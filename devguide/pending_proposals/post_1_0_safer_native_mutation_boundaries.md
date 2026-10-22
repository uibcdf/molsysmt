---
summary: Evaluate safer native mutation boundaries for interaction validity after 1.0
issue: uibcdf/molsysmt#407
status: open
opened: 2026-10-22
closed:
verification: inspected
area: [api, interactions, native]
guard:
normative:
blocked_by: []
supersedes: []
---

# Safer native mutation boundaries after 1.0

**Reported:** 2026-10-22, during maintainer review of the limits of #121.
**Status:** Open future investigation; no new mutation contract is implemented.

## What

Evaluate whether native edits that currently require explicit invalidation can
have a safer, practical supported boundary. Preserve the delivered
[copy contract](../native_copy.md) and
[interaction validity rules](../interactions_api.md). This is a post-1.0
improvement proposal, not a newly reproduced failure of a supported setter.

## How

Inventory raw array/table writes, retained writable aliases, whole-domain
replacement, direct domain append/add, private chemical-record changes and
MolecularMechanics changes. Record which operations expose mutable storage and
which can instead pass through a validated owner boundary.

Compare explicit edit transactions, owner-aware domain replacement and restricted
writable access. Choose only the routes justified by actual use cases. An
explicit invalidation requirement can remain appropriate for arbitrary external
aliases; introducing an observer wrapper does not prove those aliases are tracked.
Keep broad conservative invalidation as the correctness reference before
considering finer dependencies.

## Why

Controlled native geometry and chemistry writes already notify their molecular
owner. The normative contracts explicitly exclude raw table/array mutations and
uncoordinated domain/axis changes. The opportunity is to reduce accidental stale
analysis reuse in future workflows without rescanning complete trajectories or
copying geometry merely to detect an edit.

## What is inspected and what is assumed

**Inspected:** The boundaries and supporting guards listed in
[native copying](../native_copy.md) and
[interaction validity](../interactions_api.md), at source
`655892f7b563ab6e6d6acc07555ccf6c2d0bc082`.

**Not established:** A general observer design, its compatibility with external
NumPy/pandas aliases, or its memory and execution cost. No new timing campaign or
runtime reproduction was performed for this report.

## What was refuted

Supporting controlled setters does not observe every writable alias. Invalidating
only interactions that previously involved the moved atom is insufficient: a
previously nonparticipating atom can form a new interaction. Individual observation
editing is a different operation, owned by #335. No universal observer or chemical
dependency graph has been selected.

## Scope and exclusions

Follow the [1.0 scope freeze](../release_1_0_scope.md). Do not expand its release
gate or change existing APIs merely by filing this proposal. The concrete
`basic.remove` flag/ownership inconsistency remains independently owned by #406.
Automatic detector execution, arbitrary observation editing and large-observable
deferred copying (#405) are separate themes.

## Acceptance criteria

- Publish an inventory of covered and uncovered mutation routes and their owner.
- Define the selected edit/publication contract, explicit escape hatches and
  failure behavior before implementation; retain clear unsupported boundaries.
- Guard independent source/copy ownership, historical snapshots, evaluated-empty
  coverage, no-op edits, invalid inputs and failures around publication.
- Check atom/structure axis changes, chemistry replacement, units and multiple
  named analyses against an explicit conservative invalidation oracle.
- Compare runtime, retained memory and transient allocation with current
  controlled edits; avoid full-coordinate copies or scans on every local write.
- Update the normative API, User Guide and course for any adopted public change,
  and close with relevant behavioral guards or a normative design decision.

## Dependencies and risks

No prerequisite blocks investigation. An adopted boundary must coexist with
#121's independent-copy contract and the extraction/remapping contract. Existing
clients may rely on writable access, so access restrictions require an explicit
compatibility decision rather than silent behavior changes.
