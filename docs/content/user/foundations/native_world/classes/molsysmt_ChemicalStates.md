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
and {ref}`API Native Queries` for available resident-object queries. General
selected-state query routing is still part of the domain migration; the new
editing methods do not imply support for every molecular attribute on a
standalone collection.
