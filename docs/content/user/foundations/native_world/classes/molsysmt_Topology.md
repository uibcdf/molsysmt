(user-foundations-native-world-classes-molsysmt-topology)=
# Topology

`molsysmt.Topology` is the native data structure in MolSysMT responsible for stable atom inventories, groups, molecules, entities and represented chains.

---

## Overview and Role

As a user, `molsysmt.Topology` is the object holding stable inventory and hierarchy. Bonds, components and chemical assignments belong to the independent ChemicalStates domain. It provides fast selection queries, atom index resolution, and structural hierarchy traversals without needing 3D spatial coordinates.

---



Direct `MolSys.add` and `Topology.add` calls also validate `keep_ids` as a boolean, including its default `True`. Leave `skip_digestion=False` for ordinary public calls; trusted delegation is not required to use these methods.

## Internal Attributes

Inside `molsysmt.Topology`, data is maintained across five canonical tabular DataFrames representing stable inventory:

| Attribute | Data Frame Class | Columns / Fields | Description |
| :--- | :--- | :--- | :--- |
| **`atoms`** | `Atoms_DataFrame` | `atom_id`, `atom_name`, `atom_type`, `isotope`, `group_index`, `chain_index` | Atom inventory storing string IDs, element types, isotopes, and parent group/chain links. |
| **`groups`** | `Groups_DataFrame` | `group_id`, `group_name`, `group_type`, `molecule_index` | Group inventory specifying sequence names, group types (amino acid, water, ion), and parent molecule links. |
| **`molecules`** | `Molecules_DataFrame` | `molecule_id`, `molecule_name`, `molecule_type`, `entity_index` | Higher-level biological molecule classifications (protein, peptide, small molecule) and parent entity links. |
| **`entities`** | `Entities_DataFrame` | `entity_id`, `entity_name`, `entity_type` | Unique chemical species entities. |
| **`chains`** | `Chains_DataFrame` | `chain_id`, `chain_name`, `chain_type` | Structural chain segment labels and chain type classifications. |

---

## Invariants and Performance

`topology.copy()`, Python `copy.copy(topology)` and `copy.deepcopy(topology)` copy canonical tables
independently without accessing chemical states, preserving supported native extension state
without legacy restoration. A standalone copy does not retain its source
MolSys's weak ownership link. Copying an enclosing `MolSys` binds the copied
topology to that copied system and preserves its single chemical-state authority.
These paths copy tables eagerly. See {ref}`Independent Copies <user-foundations-molsys-copying>`.

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `molecule_id`, `entity_id`, `chain_id`) are strictly normalized and stored as **string** representations.
- **Hierarchical Index Links**: Structural parent-child relationships use integer 0-indexed vectors (`group_index`, `chain_index`, `molecule_index`, `entity_index`).
- **Chain Labels During Addition**: With `keep_ids=True`, native addition preserves explicit chain IDs and names, even when two chains share a label. Incoming positional chain indices are offset independently. `keep_ids=False` regenerates local IDs.
- **Fast Selections**: Optimized for zero-overhead Boolean evaluation by MolSysMT's internal selection parser.

---

A valid native topology can have atoms but zero groups, for example an RDKit molecule without residue metadata. In that case, atom-level `group_id`, `group_name`, and `group_type` queries return `None`; `n_groups` remains zero. MolSysMT does not invent residue groups or a ligand label. Check `msm.has_attribute(molsys, "group_name")` before requiring that hierarchy.

## Molecule Membership

An atom's molecule is a stable hierarchy assignment, independent of its covalent
component. Grouped atoms inherit `groups.molecule_index`. For atoms without a
group, `topology.set_atom_molecules(molecule_indices, atom_indices='all')`
declares positional molecule indices without creating groups or molecules.
Use `None` for unknown membership; missing information is never replaced by
the currently selected chemical state's components during a query.

There is no additional atom-table column. An optional integer vector uses eight
bytes per atom when any ungrouped assignment is known; clearing every assignment
releases that vector. Copies own their vectors. Extraction remaps retained
molecules and atom permutation retains the molecule axis. Bond edits and changes
of chemical state leave stable assignments unchanged. Initial construction from
a molecular graph can infer the hierarchy once; it is not repeated by queries.

If you assemble groups by editing tables directly, first clear obsolete ungrouped
assignments or reconcile each newly grouped position with `set_atom_molecules`.
An existing declaration cannot be silently discarded if its owner conflicts
with the new group. The supported builder performs that reconciliation for you.

A changed declaration on an attached Topology invalidates all named interaction
analyses, including evaluated-empty coverage, after successful validation.
Existing analysis snapshots remain intact; coordinates are not copied and
detectors are not run. Repeating an unchanged declaration is a no-op. Dictionary
schema 0.2 retains these declarations; legacy 0.1 reading remains available. H5MSM 0.5 preserves these
assignments in topology layer 3; see {ref}`user-tools-form-h5msm-05` and the
executed {ref}`Cookbook_Group_Free_Hierarchy` recipe.

## Container Conversion

A topology can be wrapped in a `molsysmt.MolSys` without inventing structural data:

```python
topology_only = msm.convert(topology, to_form="molsysmt.MolSys")
```

The resulting container preserves the topology with absent chemistry and structures domains. This is
useful when a workflow needs the central native container before coordinates are available.
A three-dimensional viewer has a stricter contract: converting a topology to
`nglview.NGLWidget` requires explicit `coordinates=` because MolSysMT does not fabricate a
geometry for a topology-only system.

---

## Chemical Components

Use `molsys.chemical_states.rebuild_components(topology=molsys.topology)` or the
`molsys.rebuild_components()` convenience method. `Topology` has no bonds,
components, chemical counters or chemical editing methods, even while attached
to a MolSys. A standalone collection can reconstruct its stored graph without
stable context; unsupported component names/types remain unknown.

Keep `redefine_ids=False`, `redefine_names=False` and `redefine_types=False` to
retain labels only for exactly unchanged full atom sets. Reordered component
rows follow those sets; merging/splitting cannot inherit unrelated labels.
Controlled reconstruction validates/stages data before publication. See
{ref}`ChemicalStates <user-foundations-native-world-classes-molsysmt-chemicalstates>`.

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
state. `msm.chemical_states.get_rings()` perceives a sparse minimum cycle basis from its
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

{func}`molsysmt.chemical_states.get_rotatable_bonds` classifies the complete state graph
before filtering source bond indices. Its named criteria and exclusions do not
assign chemical data or measure energy barriers. Pass explicitly chosen eligible
cuts to {func}`molsysmt.chemical_states.get_rigid_fragments` to obtain deterministic
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
molecule, entity and chain counts as `Topology`, even when it
lives in another module. Normal construction retains argument validation and
needs no digestion bypass. This does not register a separate molecular-system
form for that subclass.

## Native Queries

Query stable inventory and represented hierarchy with `topology.get(...)`. State-dependent fields require ChemicalStates or the owning MolSys as input. Native `info()` supports Styler, DataFrame and dictionary records. See {ref}`Tutorial_Get` and {ref}`Tutorial_Info`.

## Controlled Edits

Stable membership edits on an attached Topology notify its MolSys owner.
Atom-axis resizing must use a coordinated molecular edit. Chemical assignments
instead use `msm.set(molsys, ...)` or `msm.set(molsys.chemical_states, ...)`;
bond edits use `chemical_states.add_bonds()` and `remove_bonds()`.

Those chemical operations stage bonds, components and observation invalidation
before publication. Failed validation, reconstruction or allocation leaves all
unchanged. Real scientific changes invalidate all named analyses, including
previously evaluated-empty structures; no detector runs automatically. Label-only
and unchanged assignments preserve valid observations. Old snapshots remain
historical; raw pandas writes do not provide controlled edit guarantees. See
{ref}`Changing coordinates <user-tools-interactions-coordinate-edits>`.

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
Initial construction may snapshot an admitted reference-state component partition
as stable molecule membership, inheriting supported local labels and string IDs.
No biological groups or chain labels are invented. Atom-to-molecule queries read stored stable membership; another chemical state's connectivity does not silently
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


## Group Inventories

A sequence-only topology can hold known groups, their order and declared
molecule occurrences without representing any atoms. Single sequences provide
one declared occurrence; FASTA collections provide separate record occurrences.
The native conversion retains caps and group-to-molecule links and does not
synthesize representative CA atoms, chemical bonds or Cartesian coordinates.
The zero-row atom table measures represented inventory, not a chemically
established count of physical atoms. Sequence-only conversion leaves chemical_states absent; group inventory does not
provide evidence of a chemical graph.

`topology.chain_groups` exposes one ordered tuple of group indices per chain,
including empty chains. Use `topology.set_chain_groups(...)` to declare this
relation without assigning nonexistent atoms. The declaration uses compact
integer offsets and group indices, not an extra `groups.chain_index` column.
A group may belong to several chains; group-to-chain queries then return all
of them. An explicit declaration must include every observed atom/chain pair.
An empty chain has no group-mediated molecule relation; matching empty-container
row positions or names do not establish membership.
Passing `None` removes the declaration and restores atom-derived membership;
resetting the groups or chains table also clears it. Raw table edits do not
remap this relation: update it explicitly after changing the hierarchy.

Native `get()` and public `msm.get()` project represented groups, chains,
molecules and entities. Text selectors operate on that hierarchy without
building an atom table. Use `msm.extract(..., element="group", selection=[2, 0])`
for an ordered group subset, or choose `chain`, `molecule` or `entity`, including
empty declarations. With no `element`, native inventories without atoms use
groups; atomistic systems retain their atom default. Group reordering remaps
memberships; related parent tables keep source order. Repeated extraction
indices are rejected, while queries can repeat indices. Scientific operations
requiring atomic geometry or chemical assignments still require those domains.

FASTA conversion creates one chain per record. Generated IDs follow
`A` through `Z`, then `AA`, `AB`, through `AZ`, `BA`, and onward. Record tokens
remain names, full descriptions remain entity names, and the raw source report
retains the original text. Explicit source chain IDs are preserved when supplied
by a form that defines them. Copy, TopologyDict and H5MSM 0.5 retain the ordered
relation; a single one-letter string still cannot encode multiple chain boundaries.
