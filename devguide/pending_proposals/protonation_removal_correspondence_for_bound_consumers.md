---
summary: Expose public protonation-removal correspondence for managed consumers.
issue: uibcdf/molsysmt#576
status: open
opened: 2026-11-05
closed:
verification: inspected
area: [build, protonation, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Public protonation-removal correspondence for managed consumers

**Status:** proposed; public independent execution is available, managed consumer
correspondence remains unreceived. Native method and pH criteria are unchanged.

## What

Provide a public, provider-owned correspondence contract for `build.reconcile_protonation` so consumers can synchronize atom removal without importing private protonation rules, matching labels/coordinates, or running the scientific decision twice.

This is a missing integration capability, not a request to change the pH method, add detectors, or make Viewer observe arbitrary external edits. Requested under #421 / PR #543 and uibcdf/molsysviewer#264. The independent native result is already useful.

## Current evidence

Reviewed published native source `ccff2557f576f004461c96950d36a8b6e465e91f`:
- The public signature is `reconcile_protonation(molecular_system, pH=7.4, engine="MolSysMT", in_place=False, skip_digestion=False)`.
- The private `build._protonation.unexpected_hydrogens` determines the removal list, then public `basic.remove` publishes a subset.
- Default independent output has no operation-scoped public removal report; `in_place=True` returns None.
- The helper also rebuilds derived components, so it is not an approved read-only public preflight contract for consumers.

A native-only check on bundled villin (`chicken villin HP35/1vii.pdb`), explicitly extracting structure indices [0, 0, 0], gives 596 atoms at pH 7.4 and 590 at pH 12.0. The removed labels are H3 in group 0 and HZ3 in groups 7, 24, 29, 30 and 32. All three structures survive. These are bounded reference-rule checks, not environmental-pKa validation.

The existing Viewer managed-edit boundary needs trusted retained-atom correspondence before publication. Atom counts do not establish identity; atom/group IDs can repeat. A successful None result cannot provide that correspondence. Viewer must not reconstruct the provider's scientific selection from templates or private helpers.

## Requested contract

Please choose a public design that supplies:
1. Operation-scoped source indices and retained old-to-new correspondence, with explicit direction/order, universes, structures and input identity/version assumptions.
2. Assessed versus unassessed scope and the actual native reference/naming/pH parameters. Empty removal must distinguish a true no-op from unsupported/unassessed chemistry.
3. A read-only assessment/prepared-operation route available before mutation, reusable by execution without repeating the scientific decision; or an equivalent map-producing independent-result/publication contract suitable for safe integration. A post-write report alone does not satisfy the current host's prepublication mapping boundary.
4. Native independent/in-place return semantics, no-op behavior and failures, including whether candidate preparation is atomic and whether derived components/analysis coverage may change.
5. Consistent remapping/invalidation of named analyses and stored domains, without hidden charge assignment, hydrogen addition, chemical-state choice or preparation.

This does not prescribe a particular function name or force a new viewer-specific public API. A reusable native report/plan is preferable to a second protonation implementation in a consumer.

## Acceptance criteria

Add native pytest coverage for actual H removal and no-op results, unsupported/unassessed and declared named-state groups, repeated/nonunique labels, all source structures, preserved retained coordinates, map direction/uniqueness/composition, independent ownership, analysis remapping and failure/partial-publication semantics. Test that preparing the public assessment does not mutate the source and that execution consumes the same declared decision. Document the limits of fixed-pKa reference rules.

The addon can meanwhile expose the independent route and reject managed `in_place=True` before science, with that limitation explicit. This is not full in-place receiving or package qualification. No scientific native implementation is authored in Viewer.

Record through PR #543: `devguide/pending_proposals/protonation_removal_correspondence_for_bound_consumers.md`.


## Scope

The report requests a reusable public native integration contract. It does not
request automatic observation of arbitrary molecular edits or require a specific
API spelling. The consumer will receive the independent default first, with
managed in-place execution rejected before science until correspondence is qualified.
No private protonation helper or scientific inference is added to the addon.
