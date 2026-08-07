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

## API Documentation

All methods, getters, and converters for `molsysmt.Topology` are documented in the [{doc}`molsysmt.Topology API Reference </api/form/molsysmt_Topology/api_molsysmt_Topology>`].
