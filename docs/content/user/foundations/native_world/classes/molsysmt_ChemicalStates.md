(user-foundations-native-world-classes-molsysmt-chemicalstates)=
# ChemicalStates

## Overview and Role

`molsysmt.ChemicalStates` owns an ordered collection of chemical descriptions on
one atom-index domain. Each state stores bonds, nullable atom assignments and
its own components, completeness and evidence. A connected component describes
that state's graph; it is independent of stable molecule ownership in Topology.
Atom charges use elementary-charge units. Coordinates and periodic boxes belong
to Structures and are not copied by chemical graph editing.

The class remains experimental during the coordinated domain migration. Topology
still has transitional compatibility access to its collection. New selected-state
editing operates directly on ChemicalStates and never creates a Topology to hold
chemistry. See {ref}`user-foundations-native-world-classes-molsysmt-molsys` for
composition and domain correspondence.

## State Availability

A new collection contains zero states. `append_state()` explicitly creates an
unknown state; an empty bond table does not establish that no bonds exist.
No editing method creates a state implicitly. A single state resolves as the
reference. Multiple states need a declared reference or an explicit positional
`chemical_state` index. Selecting a state for one operation never changes the
reference or assigns that state to structures.

Connectivity and components independently distinguish unavailable, partial and
complete knowledge. Rebuilding an observed graph does not certify complete
chemistry. Complete connectivity with known participation can yield a complete
component partition, including isolated atoms and an empty edge set.

## Stored Queries

Use `chemical_states.get(..., chemical_state=...)` or
`msm.get(chemical_states, ..., chemical_state=...)` to read stored indices,
counts and completeness without constructing Topology. System-level `n_bonds`
and `n_components` refer to the selected state. `chemical_state_index`,
`chemical_state_id` and `n_chemical_states` describe the whole collection;
`reference_chemical_state_index` reports its reference without changing it.

| Source element | Available indices and counts |
| :--- | :--- |
| `system` | Shared `n_atoms`; selected-state `n_bonds` and `n_components`; collection inventory and reference. |
| `atom` | `atom_index`, nullable `component_index`, incident `bond_index`, selected length `n_atoms`, per-atom incident `n_bonds`, and distinct declared `n_components`. |
| `component` | `component_index`, member `atom_index`, per-component `n_atoms` and incident `n_bonds`, and selected length `n_components`. |
| `bond` | `bond_index` in the selected state's own bond table. |

Explicit selections retain order and repetitions. Masks produce a sorted set
intersection, as in `basic.get`. Bond/component bounds are resolved in the
selected state. Boolean flags belong in masks, not mixed into index lists.
Empty selections retain defined scalar/list shapes. Declared components with
no atom members remain visible; unknown membership is not assigned to a new
component. An explicit atom selection counts distinct known components, while
`selection='all'` counts the full declared component inventory.

`connectivity_completeness`, `component_completeness` and `component_evidence`
return the selected state's stored declaration. Zero edges can be unavailable,
partial or complete knowledge. Queries do not rebuild components, infer bonds
or certify preparation. A zero-state collection still has an atom domain and
state inventory, but querying its chemical counts raises an unavailable-state
error. A missing reference with multiple states requires an explicit index.

`info()` summaries currently follow reference-state rules. These capabilities
do not yet include standalone rich chemical fields, state-aware dictionary
query dispatch or stable group/chain/molecule context. A query needing such
absent context cannot reconstruct it from component membership.

## Controlled Editing

`add_bonds`, `remove_bonds` and `rebuild_components` edit only the selected state.
They stage validation, bond/component tables and required analysis invalidation
before publishing. A failure preserves the original chemistry and analyses.
Other states, atom assignments, producer histories, the reference and structure
associations remain intact. Previously obtained tables and analysis snapshots
remain their old values when a supported edit replaces current data.

An owning MolSys supplies stable topology context for component labels. A
standalone collection can instead receive an explicit matching Topology. The
context is never mutated or queried for chemical storage; supplying it declares
positional atom correspondence. Without adequate context, names/types stay
missing. Unrequested labels survive reconstruction only for exactly unchanged
full atom sets. Merged or split components cannot inherit those labels.

Graph or completeness changes conservatively invalidate all named analyses of
the owner, including structures evaluated without occurrences. Empty additions,
empty removals and removal from an already empty table are no-ops after state
resolution. Label-only reconstruction preserves interaction observations.
No detector, hydrogen placement, aromaticity perception or preparation runs
automatically. See {ref}`Tutorial_Native_Chemical_Editing` and
{ref}`Cookbook_Group_Free_Hierarchy` for supported operations and executed examples.

## Table Boundaries

`get_bonds(chemical_state=...)` returns the selected state's live table for reading
and interchange. Direct Pandas/NumPy writes bypass validation, component
reconstruction and owner notification. Use controlled graph methods or existing
`basic.set` assignment routes on an owning MolSys. Standalone assignment dispatch
is still being migrated. A live table does not provide a universal
mutation-observation mechanism.

Supported metadata assignments validate before publishing and retain other
states. A `bond_id` assignment changes only a string label: it preserves bond
positions, nullable columns and interaction observations. Scientific assignment
changes invalidate the owning system's observations. Reading a stored assignment
does not repair or rewrite its source data.

Copies own their chemical records. `ChemicalStatesDict` retains typed columns
and null masks, and H5MSM 0.5 stores chemistry independently of topology and
structures; see {ref}`user-tools-form-h5msm-05`. Restriction and historical index
scope are described in {ref}`Tutorial_Extract`.

## API Documentation

See {ref}`API Native Chemical Editing` for exact signatures and failure behavior,
and {ref}`API Native Queries` for available resident-object queries. Further
chemical-attribute and assignment routing remains part of the domain migration;
the stored-axis queries do not imply support for every molecular attribute on a
standalone collection.
