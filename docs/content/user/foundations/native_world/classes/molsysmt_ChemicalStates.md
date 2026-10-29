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
counts, stored assignments and completeness without constructing Topology. System-level `n_bonds`
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

`info()` summaries currently follow reference-state rules. State-aware dictionary
query dispatch and stable group/chain/molecule context are still being migrated.
A query needing absent context cannot reconstruct it from component membership.

## Stored Assignments

Atom queries can read `formal_charge`, `atom_is_aromatic`,
`n_unpaired_electrons`, `n_implicit_hydrogens`, `n_explicit_hydrogens`,
`allows_implicit_hydrogens` and `atom_stereochemistry`. These are stored
assignments: reading hydrogen counts does not recount atoms or bonds, and reading
aromaticity does not run perception. An absent atom-property column returns
`None`. A materialized column returns one value per selected atom, with `None`
for unknown values and `[]` for an empty selection. Zero and False are known
values. `has_attribute(..., chemical_state=...)` checks the selected state's
nonmissing values; `include_none=True` asks about the supported delivery route.

Formal charge retains the established integer schema: each value is an integer
multiple of the elementary charge, not a partial charge or a unit-bearing
quantity. `get(formal_charge=True)` returns the atom vector, not its sum.
This ownership migration does not change the charge-unit policy.

Use `element='bond'` for `bond_id`, `bond_order`, `fractional_bond_order`,
`bond_type`, `bond_is_aromatic`, `bond_is_conjugated`, `bond_stereochemistry`,
`bond_stereo_atom_indices`, `bond_donor_atom_index`, `bond_acceptor_atom_index`,
`bond_joins_components` and `bond_evidence`. Optional missing fields return
one `None` per selected edge. Stereo references return two independently nullable
atom indices per edge, including `[None, None]` if neither is known. Empty bond
selections return `[]`. Bond order is dimensionless; direction and component
participation are read as declared, never inferred during querying.

`component_id`, `component_name` and `component_type` can be read from
`element='component'` or projected to `element='atom'`. Unknown component
membership gives `None`, even if other component rows have labels. Bond and
component IDs remain string labels, independent of positional indices. All these
queries retain ordered repetitions, selected-state bounds and source tables.
Component assignment dispatch and chemical predicates remain separate pending
work; query support does not make live-table mutation a validated edit.

## Assigning State Fields

Use `msm.set(chemical_states, ..., chemical_state=...)` to assign the seven atom
properties and twelve bond fields listed above. An omitted `element` follows the
attribute's atom/bond destination. Explicit integer positions are unique and
values follow their supplied order. Scalars broadcast; `None` assigns unknown
values, retaining nullable columns. A first subset atom assignment leaves other
atoms unknown. No state, edge or atom is created implicitly. Empty selections
change nothing after state resolution. Invalid or ambiguous states reject.

Integer formal charges accept counts representable as Int16 or one-dimensional
charge quantities. Quantities are converted explicitly to elementary charge
before storing integer counts, independently of application standard units.
Hydrogen and unpaired-electron counts use UInt8. Boolean flags cannot stand in
for integer counts. Incompatible units, fractions, nonfinite charge quantities
and overflow reject.

Each attribute is validated and staged before publication. Rejection preserves
source tables and analyses; other states, coordinates, the reference, structure
associations and history stay intact. Supported assignments through
`molsys.chemical_states` notify that owner, conservatively invalidating all named
analyses, including evaluated-empty coverage. Changing only `bond_id` preserves
observations and bond-row layout. Returned old tables retain their old values.
A call with several attributes performs separate assignments; it is not one
transaction across those attributes.

Bond fields use existing canonical validation. Set stereo references before a
stereochemical label requiring them, and evidence before a nondefault component
participation flag. Metadata assignment does not rebuild components; explicitly
call `rebuild_components` after changing participation if you need the partition
of the modified graph. This differs from `add_bonds` and `remove_bonds`, which
coordinate graph editing and reconstruction. Standalone component membership and
label setters, dictionary assignment and mixed-owner cutover remain pending.

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
`basic.set` atom/bond assignment routes on the collection or its owning MolSys.
A live table does not provide a universal
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
