---
summary: Review the finite MolSysMT facts and maps for BindingSite region projection
issue: uibcdf/molsysmt#746
status: resolved
opened: 2026-11-13
closed: 2026-11-13
verification: measured
area: [api, basic, native]
guard: tests/basic/test_binding_site_membership_handoff.py
normative: devguide/native_binding_site_membership_contract.md
blocked_by: []
supersedes: []
---

# Finite molecular facts for BindingSite membership

## What

BindingMT #111 requests actual public facts and guarantees for source-index
membership, group expansion, native extraction/permutation maps, repeated
structure occurrences, explicit states, and omitted/generated members.
Its `e1e6a337` profile is declaration-only and does not qualify molecular
resolution. The earlier #734 contact/SASA review supplies useful existing
facts but is not acceptance of this additional profile.

## How

The [normative owner contract](../../native_binding_site_membership_contract.md)
records the callable/fact/check/precondition/refusal table. It uses native and
generic public get/select/extract/permute/compose routes without a new matcher,
serializer, observer or universal receipt. Counts and map validity are not
source authentication or revision/current-finding guarantees.

New independent six-atom/three-group/three-structure examples use duplicate
string labels, noncontiguous group membership, two chemical states, literal
permutation/inverse expectations, `[2,0,2]` occurrences, and H5MSM readback under
nm/ps and pm/fs. A real terminal-atom attachment supplies a generated current
member with no original atom identity. Missing and contradictory maps refuse;
partial maps retain omissions for the client's coverage policy.

## Why

A consumer must retain declared entry order while molecular extraction sorts
atoms and rebuilds group rows. A source structure can have multiple target
occurrences. Independent one-to-one atom maps cannot encode that inverse
structure relation. Unknown parentage and changed coordinates can coexist with
unchanged counts/labels, so their agreement must not certify common origin or
complete/current scientific applicability.

## Outcome and evidence

Existing public tools supply the admitted membership/correspondence facts.
The concrete numeric/all selection-boundary defect found here is fixed under
#750 with reused validation. No additional new molecular-operation gap is
established. The selected receiving passes 356 cases, without omissions,
including new/reused native query, state, map, selection and #734 controls.
The final 18-case owner module adds literal associated-charge checks after
readback; these scopes overlap and are not summed as independent full suites.
The [receipt](../../../devtools/data/binding_membership_receiving_746_750_20261113.json)
retains actual inputs/outcomes, original test-draft import errors, negative
bounds cases and bounded shared-host resources.

The registered BindingMT checkout is missing; its immutable public declaration
documents were read and verified against Git blob hashes instead. Historical
DockingMT working files stay untouched. No client is installed or modified.
No runtime/provider/native dependency or scientific algorithm changes beyond
#750's existing selection-boundary repair.

## Acceptance and remaining ownership

The owner review is complete with its maintained normative contract, public
examples and meaningful guard. BindingMT still reviews and qualifies its actual
`resolve_region` composition and persistence; this closure does not certify
consumer adoption, current binding findings, C2 geometry or other components.
A later concrete missing fact requires its own bounded owner request. Mandatory
full/nightly, installed/platform/final-pair and publication gates remain separate.
This review adds no new pre-1.0 feature or global release prerequisite.
