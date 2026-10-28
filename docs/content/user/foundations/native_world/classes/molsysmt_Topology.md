(user-foundations-native-world-classes-molsysmt-topology)=
# Topology

`molsysmt.Topology` is the native data structure in MolSysMT responsible for managing atom inventories, residue groups, molecular entities, chemical chains, and covalent bonding graphs.

---

## Overview and Role

As a user, `molsysmt.Topology` is the object holding all structural identity and chemical metadata for a system. It provides fast selection queries, atom index resolution, and structural hierarchy traversals without needing 3D spatial coordinates.

---



Direct `MolSys.add` and `Topology.add` calls also validate `keep_ids` as a boolean, including its default `True`. Leave `skip_digestion=False` for ordinary public calls; trusted delegation is not required to use these methods.

## Internal Attributes

Inside `molsysmt.Topology`, data is maintained across seven canonical tabular DataFrames representing the structural hierarchy and chemical bonding state:

| Attribute | Data Frame Class | Columns / Fields | Description |
| :--- | :--- | :--- | :--- |
| **`atoms`** | `Atoms_DataFrame` | `atom_id`, `atom_name`, `atom_type`, `isotope`, `group_index`, `chain_index` | Atom inventory storing string IDs, element types, isotopes, and parent group/chain links. |
| **`groups`** | `Groups_DataFrame` | `group_id`, `group_name`, `group_type`, `molecule_index` | Residue and group inventory specifying sequence names, group types (amino acid, water, ion), and parent molecule links. |
| **`components`** | `Components_DataFrame` | `component_id`, `component_name`, `component_type` | Connected covalent graph components. |
| **`molecules`** | `Molecules_DataFrame` | `molecule_id`, `molecule_name`, `molecule_type`, `entity_index` | Higher-level biological molecule classifications (protein, peptide, small molecule) and parent entity links. |
| **`entities`** | `Entities_DataFrame` | `entity_id`, `entity_name`, `entity_type` | Unique chemical species entities. |
| **`chains`** | `Chains_DataFrame` | `chain_id`, `chain_name`, `chain_type` | Structural chain segment labels and chain type classifications. |
| **`bonds`** | `Bonds_DataFrame` | `atom1_index`, `atom2_index`, `bond_id`, `bond_order`, `bond_type`, `is_aromatic`, `is_conjugated` | Covalent bond graph specifying bonded atom index pairs, bond orders, and aromaticity flags. |

---

## Invariants and Performance

`topology.copy()`, Python `copy.copy(topology)` and `copy.deepcopy(topology)` copy canonical tables
and chemical states independently, preserving supported native extension state
without legacy restoration. A standalone copy does not retain its source
MolSys's weak ownership link. Copying an enclosing `MolSys` binds the copied
topology to that copied system and preserves its single chemical-state authority.
These paths copy tables eagerly. See {ref}`Independent Copies <user-foundations-molsys-copying>`.

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `molecule_id`, `component_id`, `entity_id`, `chain_id`, `bond_id`) are strictly normalized and stored as **string** representations.
- **Hierarchical Index Links**: Structural parent-child relationships use integer 0-indexed vectors (`group_index`, `chain_index`, `molecule_index`, `entity_index`).
- **Chain Labels During Addition**: With `keep_ids=True`, native addition preserves explicit chain IDs and names, even when two chains share a label. Incoming positional chain indices are offset independently. `keep_ids=False` regenerates local IDs.
- **Fast Selections**: Optimized for zero-overhead Boolean evaluation by MolSysMT's internal selection parser.

---

A valid native topology can have atoms and bonds but zero groups, for example an RDKit molecule without residue metadata. In that case, atom-level `group_id`, `group_name`, and `group_type` queries return `None`; `n_groups` remains zero. MolSysMT does not invent residue groups or a ligand label. Check `msm.has_attribute(molsys, "group_name")` before requiring that hierarchy.

## Container Conversion

A topology can be wrapped in a `molsysmt.MolSys` without inventing structural data:

```python
topology_only = msm.convert(topology, to_form="molsysmt.MolSys")
```

The resulting container preserves the complete topology and has zero structures. This is
useful when a workflow needs the central native container before coordinates are available.
A three-dimensional viewer has a stricter contract: converting a topology to
`nglview.NGLWidget` requires explicit `coordinates=` because MolSysMT does not fabricate a
geometry for a topology-only system.

---

## Rebuilding Components

`topology.rebuild_components()` reconstructs the resolved chemical state's
atom-level component indices from stored bond participation. Its default flags
regenerate local string IDs and infer names/types. Set `redefine_ids=False`,
`redefine_names=False` and `redefine_types=False` to retain those fields for
components whose atom sets are exactly unchanged, even if component row indices
are reordered. Merged, split or unresolved components cannot inherit those labels;
their unrequested metadata remains missing. Other chemical states are untouched.
Preserving labels does not certify complete connectivity or chemical identity.
`molsys.rebuild_components(redefine_ids=False, redefine_types=False)` delegates to
the same operation while continuing to infer names.

---

## Covalent Walks

Pattern-based covalent queries retain full source atom indices. A selected
subset restricts candidates without renumbering the source. Each pattern
position defines one column of the result: no matches retain an empty row
axis and the complete pattern width. This allows downstream recognition, such
as donor–hydrogen pairing, to distinguish valid no-match results from invalid
selectors without inventing bonds or hydrogens. A pattern-matching walk may
revisit atoms; it does not measure a shortest-path distance. See
{ref}`Tutorial_Get_covalent_paths` for executed examples.

## Ring Participants

Covalent connectivity and aromatic flags belong to the selected `ChemicalStates`
state. `msm.topology.get_rings()` perceives a sparse minimum cycle basis from its
covalent graph. `msm.physchem.get_aromatic_rings()` perceives a basis from the
explicitly aromatic bond subgraph. Both preserve source atom indices, return
complete sorted memberships, and reject selections cutting a perceived ring.
A cycle basis need not be unique; it is not every cycle. Declared aromaticity,
geometric planarity, and observed interactions have distinct meanings. Unknown
aromatic flags require explicit chemistry before recognition. These experimental
operations do not calculate contacts or alter the source state. See
{ref}`Tutorial_Get_rings`, {ref}`Tutorial_Get_aromatic_rings`, and
{ref}`Cookbook_Preparing_aromatic_participants` for executed examples.

---

## Torsion Candidates

{func}`molsysmt.topology.get_rotatable_bonds` classifies the complete state graph
before filtering source bond indices. Its named criteria and exclusions do not
assign chemical data or measure energy barriers. Pass explicitly chosen eligible
cuts to {func}`molsysmt.topology.get_rigid_fragments` to obtain deterministic
packed memberships. Docking workflows choose active cuts and rooted export
separately. See {ref}`Tutorial_Rotatable_Bonds` for exact criteria and limits.

## API Documentation

See {ref}`API Native Queries` for resident-object queries and
{func}`molsysmt.basic.convert` for form-agnostic conversion.

Native copying preserves distinct parent/child slot storage and graph aliases,
and omits the old owner even when stored in a slot. Canonical molecular columns
are independent; arbitrary mutable cells and pandas metadata follow pandas'
own copy protocols. This does not add persistent schema fields.

## Inherited Construction

A subclass inheriting the native constructor accepts the same atom, group,
component, molecule, entity, chain and bond counts as `Topology`, even when it
lives in another module. Normal construction retains argument validation and
needs no digestion bypass. This does not register a separate molecular-system
form for that subclass.

## Native Queries

Query its atom/group hierarchy and state-dependent attributes with `topology.get(...)`. `chemical_state` follows the basic query rules; ChemicalStates remains the owner of assignments and bonds. Native `info()` supports Styler, DataFrame and dictionary records. See {ref}`Tutorial_Get` and {ref}`Tutorial_Info`.

## Controlled Edits

When a topology belongs to a `MolSys`, chemical-state assignments through
`msm.set(molsys.topology, ...)` notify that owner. This covers formal charges,
aromaticity, hydrogen/radical assignments, atom/bond stereochemistry, scientific
bond fields and component membership. Native `add_bonds()` / `remove_bonds()`
and replacing the `bonds` table notify it too. Changed chemistry makes every
named analysis unevaluated, including previously evaluated-empty structures;
earlier result/query snapshots survive. No detector runs automatically.

Values are validated and prepared before publication. Invalid assignments or
failure to allocate invalidation leave chemical values and analyses unchanged.
Bond IDs and empty selections do not invalidate. Bond addition/removal rebuilds
components after publishing bonds; a rebuilding failure can leave changed bonds
with analyses already invalidated. Old table handles do not follow replacement.
Reserving empty bond rows does not declare partial connectivity; removing
bonds preserves the existing connectivity-completeness declaration.
Appending a state to the owning system's `chemical_states` also invalidates all
analyses; appending preparation history preserves them because it only archives
evidence. Raw cell/array edits, other private chemical-state collection changes
and whole-topology replacement still need explicit owner invalidation. Standalone topology copies
have no owner link. See {ref}`Changing coordinates <user-tools-interactions-coordinate-edits>`
for the shared analysis validity policy.

## Sequence correspondence

Groups are the general molecular inventory, not a list of sequence letters.
A terminal cap, water or ligand keeps its original group index even though
amino-acid sequence projection omits it. Native one-letter conversion and
sequence identity share that projection. Identity reports matched source group
indices in each input, so extraction or reordering of a source changes the
indices that belong to that new source. Group IDs remain labels.

Identity is normalized by the number of query letters; empty sequence selections
raise explicitly. See {ref}`the sequence identity tutorial <Tutorial_Get_sequence_identity>`
and {ref}`the source-group comparison recipe <Cookbook_Sequence_source_groups>`.


## Group-free molecules

A complete atom inventory may have no group hierarchy, as with an RDKit graph.
Native molecule rebuilding uses reference-state components as its fallback
molecule partition, inheriting local names/types and generating string IDs.
No biological groups or chain labels are invented. Atom-to-molecule queries
reuse that partition; another chemical state's connectivity does not silently
redefine the stable molecular axis. Existing group-based molecular definitions
retain their own membership. Direct MolSysDict conversion preserves explicitly
absent groups and validates group-free molecule records against the fallback.
Builders decoded from such records, or initialized from a native group-free
molecule inventory, retain that absence when built. Empty incremental builders
keep their usual grouping defaults.


## Sequence Sources

A submitted FASTA occurrence is not a molecular group or a verified chemical
realization. Source-preserving FASTA inspection retains full headers, original
text and record-character spans before normalized sequence conversion. Empty
and repeated records remain independently addressable. These source axes do
not create a topology or imply molecular identity; the application decides
which sequence view is admissible. See
{ref}`FASTA ingestion <Tutorial_Form_file_fasta>`.
