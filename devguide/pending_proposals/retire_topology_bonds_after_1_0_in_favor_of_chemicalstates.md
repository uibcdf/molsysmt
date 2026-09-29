---
summary: Retire Topology.bonds after 1.0 in favor of ChemicalStates
issue: uibcdf/molsysmt#255
status: open
opened: 2026-09-29
closed:
verification: inspected
area: [api, form, docs]
guard:
normative:
blocked_by: [uibcdf/molsysmt#254]
supersedes: []
---

# Retire Topology.bonds after 1.0 in favor of ChemicalStates

**Reported:** 2026-09-29, while separating the public chemical-state domain
from the stable topology before 1.0.
**Status:** Open for a release after 1.0; no removal is proposed for the 1.0
candidate.

## What

Retire the public `Topology.bonds` compatibility property after 1.0 so that
covalent bonds are obtained from `MolSys.chemical_states` or a standalone
`ChemicalStates` object. `Topology` should ultimately describe stable atom
inventory and hierarchy without presenting a state-dependent bond table as
one of its own attributes.

This is a recommendation and a future API decision. The release that removes
the property must obey the compatibility guarantees established by 1.0;
if `Topology.bonds` is stable in that release, removal belongs in a later
breaking-version window.

## How

1. Inventory readers, setters, native builders, form adapters, file
   converters, notebooks, and downstream clients that use `Topology.bonds`
   or the related bond-mutating methods. Record which operations need a
   reference chemical state and which require an explicit state index.
2. Provide equivalent operations on `ChemicalStates` and a way to resolve a
   structure's state through `MolSys`. Define the behavior of a standalone
   `Topology` without any chemical-state domain.
3. Publish a compatibility and migration policy before removal. Update the
   public form and attribute contracts, documentation, Four Paths examples,
   and conversion-fidelity behavior together with the implementation.
4. Remove the facade and its setter only in the selected post-1.0 release;
   test that bond queries and edits use the intended chemical-state object
   without creating a second bond authority.

## Why

`Topology.bonds` currently exposes the reference state's bond table and is
used by existing workflows. It is a compatibility facade over chemical-state
data, not stable topological inventory. Its presence makes a state-dependent
quantity appear to belong to `Topology` and obscures whether the reference
state is absent, ambiguous, or explicitly selected. The independent
`ChemicalStates` domain under `uibcdf/molsysmt#254` provides the destination
for the eventual migration.

## What is measured and what is assumed

- **Inspected:** `Topology.bonds` is a property of the native topology and
  currently resolves the selected reference state's bond table. User Guide,
  course, native tests, and conversion paths reference it.
- **Assumed:** removing the facade will simplify the public model for users.
  This usability claim needs client feedback before implementation.
- No performance claim is made; performance is not the reason for the proposal.

## What was refuted

- Removing `Topology.bonds` before 1.0 is not the agreed boundary. The
  pre-1.0 plan preserves it for existing workflows while removing the public
  `Topology.chemical_states` property.
- Removing only the getter while retaining bond-mutating entry points would
  leave the ownership model unclear. Those methods need an explicit inventory
  and disposition before the final API change.

## Scope and exclusions

This issue concerns the public bond facade and the migration needed to retire
it after 1.0. It does not remove covalent bond data, reinterpret observed
interactions as bonds, change the H5MSM 0.4 compatibility reader, or block the
pre-1.0 work on H5MSM 0.5 and `Interactions`.

## Acceptance criteria

1. The release and compatibility policy is explicit, including any
   deprecation period and the breaking-version boundary.
2. Every public `Topology.bonds` read/write route and related bond mutator has
   a documented destination or a documented removal decision.
3. `ChemicalStates` and `MolSys` cover the needed bond and state-selection
   workflows, including no state, one state, and ambiguous multiple states.
4. Native objects, form adapters, legacy file reads, User Guide, Cookbook,
   Four Paths, and known consumers pass their relevant migration tests.
5. Durable rules move into a normative document; archive this proposal and
   close `uibcdf/molsysmt#255` with the release decision and a behavioral
   guard or normative-document reference.

## Dependencies and risks

`uibcdf/molsysmt#254` must establish independent chemical-state ownership
before the compatibility facade can be retired. Clients that directly mutate
`Topology.bonds` need a replacement API and a migration interval. A release
that silently changes the meaning of a legacy bond getter would be a
scientific correctness regression.
