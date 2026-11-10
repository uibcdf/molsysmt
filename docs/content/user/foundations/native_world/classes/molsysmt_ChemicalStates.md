(user-foundations-native-world-classes-molsysmt-chemicalstates)=
# ChemicalStates

## Overview and Role

`molsysmt.ChemicalStates` owns an ordered collection of chemical descriptions on
one atom-index domain. Each state stores bonds, nullable atom assignments and
its own components, completeness and evidence. A connected component describes
that state's graph; it is independent of stable molecule ownership in Topology.
Atom charges use elementary-charge units. Coordinates and periodic boxes belong
to Structures and are not copied by chemical graph editing.

The class remains experimental. Selected-state editing operates directly on
ChemicalStates. Topology owns stable inventory and has no chemical facade,
including while attached to MolSys. See {ref}`user-foundations-native-world-classes-molsysmt-molsys` for
composition and domain correspondence.

## Declared and Inferred Reader Connectivity

CIF/BCIF native conversion with `get_missing_bonds=False` retains mapped
component-bond and supported connection declarations without reconstructing
missing edges from templates, terminal H names, polymer sequence or distance.
The returned state is partial: an explicit edge list is not certification that
all chemical connectivity was declared. Unknown orders remain unknown. Original
observations and stable inventory are separate from these chemical claims.

With the default `True`, the reader keeps its existing inferred additions and
explicit/inferred evidence distinction. A partial reference match must not erase
a deposited edge or its known order. See
{ref}`Tutorial_Form_mmcif_PdbxContainers_DataContainer` for the reader contract.

PDB reading also retains a typed, per-declaration audit in the chemical-state
preparation history. A missing/ambiguous endpoint, unrepresented symmetry image
or contradictory sulfur partnership is different from an ordinary redundant
record. Alternate serials retain their canonical-site correspondence and their
conditional source scope. This is deposited evidence, not chemical validation.
The original operation's indices remain historical when you extract or reorder
the system; use current bond tables for the current index domain. See
{ref}`cookbook-pdb-connectivity-policy` for inspecting this evidence.

Native H-parent inference can explicitly consult bundled, versioned H-name
alternatives. That lookup changes no atom/group labels or naming declarations;
its resource, bibliography and original source indices belong to the operation's
history. Parent agreement does not assign stereochemical H roles, protonation
or a complete terminal state. See {ref}`Tutorial_Covalent_Bond_Candidates`.

Local terminal-cap references also require explicit source context. Stored
`amber` or `legacy` declarations let the shared auditor compare ACE/NME/NHE/NH2
inventories and cap roles before bounded connectivity inference. Bare labels do
not establish that interpretation. Reference identity and inferred edges belong
to the operation history and selected chemical state; stable group naming
declarations remain in Topology. This does not assign a biological terminus,
add a cap or certify a terminal/protonation state. See
{ref}`Tutorial_Residue_Chemical_Coverage`.

## State Availability

An explicit CCD reference can be constructed without coordinates through
{func}`molsysmt.physchem.get_chemical_template`. Its chemical assignments and
historical construction report belong to ChemicalStates; names and original
element inventory belong to Topology. Neither CCD model coordinates nor a
reference's chemical state replace an observed pose or determine its bound
protonation. Inspect missing/conflicting declarations and validate an explicit
correspondence before application. See {ref}`Tutorial_Get_Chemical_Template`.

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

Component IDs, names and types can be compared explicitly through
`msm.compare(molsys_A, molsys_B, component_type=True)` and the corresponding
ID/name flags. These compare reference-state labels without rewriting tables;
matching labels alone do not certify chemical equivalence. A False flag tests
inequality, and `output_type="dictionary"` exposes each result. See
{ref}`Tutorial_Compare` for the query and missing-value contract.

The experimental indexed-H policy operation can close implicit-H permission on
already indexed neutral terminal H, without adding atoms or selecting protonation.
It requires an available declared inventory and preserves isotope/stereo labels,
other states and source assignments. Every success appends original operation
evidence; a changed result invalidates analyses only on its independent returned
system. Geometry uses protected deferred copying. See
{ref}`Tutorial_Normalize_Indexed_Hydrogen_Policy` for exact admission, memory and
historical-index limits.

## Chemical and structural scope

Chemical-site recognition can use stored chemistry without coordinates. Its
`structure_indices` still refer to the original source axis when supplied
explicitly; boolean values are not positional indices. For
`msm.interactions.hbonds.get_hbond_sites`, `None` means `all`. An empty structure
scope does not erase reference/explicit-state chemical sites, but cannot resolve
an assigned state or evaluate a spatial selection. A spatial selection needs
coordinates and uses the first requested structure, including after an H5MSM
read. This scope is distinct from an interaction analysis's evaluated coverage.
See {ref}`Tutorial_Get_hbond_sites`.

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

`info()` summaries currently follow reference-state rules. The typed dictionary
offers direct stored queries; see
{ref}`ChemicalStatesDict <user-foundations-native-world-classes-molsysmt-chemicalstatesdict>`.
Mixed queries on MolSys combine its independent stable and chemical domains.
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
General chemical predicates and dictionary editing remain separate pending work;
query support does not make live-table mutation a validated edit.

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
and overflow reject. Unsupported bare inputs, including fractional floats,
raise `ArgumentError` naming `formal_charge` before an assignment is published.
The stored values, attached analyses and caller unit policy remain unchanged.

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
coordinate graph editing and reconstruction. Dictionary assignment and mixed-owner
cutover remain pending.

## Component Declarations

`msm.set(chemical_states, component_index=..., chemical_state=...)` declares
atom membership in the selected state's **existing component rows**. Scalars
and one-item vectors broadcast; other vectors follow the unique selected atom
positions. None means unknown membership. Out-of-range references reject; this
operation never creates, removes or compacts component rows. A zero-state
collection requires an explicit state, and an unknown state with no component
inventory cannot accept index 0. Existing inventory can come from an imported
declaration or explicit `rebuild_components` over the observed graph.

A changed membership declaration records `component_evidence='user_defined'` and
`component_completeness='partial'`, or `'unavailable'` when every membership is
unknown. It does not certify agreement with the bond graph or alter connectivity
completeness, atom assignments, bonds or stable molecule ownership. Explicit
reconstruction evaluates the stored graph with its existing participation rules.
Identical declarations and empty selections preserve tables and analyses.

Labels survive a membership change only when the **entire atom set** of a new
component equals an old component's full atom set. Labels follow that set even
when its index changes. Changed, merged or split sets receive missing IDs, names
and types. Empty/unknown sets cannot establish a unique correspondence, so their
labels also become unknown after a changed declaration. Stored row count remains
unchanged, including rows with no assigned atoms; an explicit atom selection can
still count distinct known memberships separately from the inventory size.

The component-ID assignment contract also applies through an owning MolSys and
ChemicalStatesDict. Scalar lexical IDs retain their spelling, numeric IDs become
strings, and None clears selected labels; Boolean labels reject. Text such as
`"1 nm"` is an opaque ID rather than a physical quantity. Indices remain positions.

Use `component_id`, `component_name` or `component_type` to assign labels on
`element='component'` (also the inferred destination). None clears a label;
scalars and one-item vectors broadcast. IDs normalize integer labels to strings
and retain lexical spelling such as `'001'`; names/types require strings.
`element='atom'` updates the whole component row of each selected atom, including
its unselected members. Selected atoms need known membership. Multiple atoms of
one component must supply the same label; conflicts reject before publication.

Label-only edits preserve observation objects and completeness/evidence. Changed
membership conservatively invalidates every named analysis of the owning MolSys,
including evaluated-empty coverage. Membership, metadata correspondence and
invalidation are staged together, so failure preserves the original tables,
other states, history, reference, structure associations and coordinate arrays.
These are per-attribute guarantees; a call with several attributes performs
separate edits. A declaration does not run chemical preparation or graph inference.

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

Typed ChemicalStatesDict field assignments use the same controlled native rules
through `msm.set`, materializing only the selected state before publication.
Graph-editing methods still require explicit conversion to ChemicalStates.
`contains` and `is_composed_of` accept `chemical_state` for supported state-local
counts; they do not supply absent stable hierarchy.

## Recognizing observed peptide endpoints

With stable group/chain context, {func}`molsysmt.chemical_states.get_peptide_termini` reads a selected stored backbone graph. It uses bonds rather than ID labels or storage order, records cap attachments and refuses ambiguous paths. This observed-graph result does not certify complete chemistry or reconstruct missing links. See {ref}`Getting peptide termini <Tutorial_Get_peptide_termini>`.
