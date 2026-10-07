(user-foundations-native-world-classes-molsysmt-topology)=
# Topology

`molsysmt.Topology` is the native data structure in MolSysMT responsible for managing atom inventories, residue groups, molecular entities, chemical chains, and covalent bonding graphs.

---

## Overview and Role

As a user, `molsysmt.Topology` is the object holding all structural identity and chemical metadata for a system. It provides fast selection queries, atom index resolution, and structural hierarchy traversals without needing 3D spatial coordinates.

---

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

- **String Identifier Invariant**: All element IDs (`atom_id`, `group_id`, `molecule_id`, `component_id`, `entity_id`, `chain_id`, `bond_id`) are strictly normalized and stored as **string** representations.
- **Hierarchical Index Links**: Structural parent-child relationships use integer 0-indexed vectors (`group_index`, `chain_index`, `molecule_index`, `entity_index`).
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

All methods, getters, and converters for `molsysmt.Topology` are documented in the [{doc}`molsysmt.Topology API Reference </api/form/molsysmt_Topology/api_molsysmt_Topology>`].
