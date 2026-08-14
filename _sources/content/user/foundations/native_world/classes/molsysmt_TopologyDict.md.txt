(user-foundations-native-world-classes-molsysmt-topologydict)=
# TopologyDict

`molsysmt.TopologyDict` is the native declarative dictionary representation of molecular topology in MolSysMT.

---

## Overview and Role

`molsysmt.TopologyDict` provides a lightweight, JSON-serializable dictionary schema wrapped by the `TopologyDict` dataclass. It represents atoms, residues, components, molecules, entities, chains, and covalent bonds without needing DataFrame instances.

---

## Declarative Schema

The underlying `data` dictionary of `TopologyDict` contains envelope headers and lists of primitive item dictionaries:

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"format"`** | String (`"molsysmt"`) | Framework format identifier tag. |
| **`"kind"`** | String (`"topology"`) | Topology category classifier. |
| **`"version"`** | String (`"0.1"`) | Schema specification version string. |
| **`"metadata"`** | Dictionary | User-defined topology provenance metadata. |
| **`"atoms"`** | List of Dicts | Atom item dictionaries containing `atom_id`, `atom_name`, `atom_type`, `isotope`, `group_index`, `chain_index`. |
| **`"groups"`** | List of Dicts | Group dictionaries containing `group_id`, `group_name`, `group_type`, `molecule_index`. |
| **`"components"`** | List of Dicts | Component dictionaries containing `component_id`, `component_name`, `component_type`. |
| **`"molecules"`** | List of Dicts | Molecule dictionaries containing `molecule_id`, `molecule_name`, `molecule_type`, `entity_index`. |
| **`"entities"`** | List of Dicts | Entity dictionaries containing `entity_id`, `entity_name`, `entity_type`. |
| **`"chains"`** | List of Dicts | Chain dictionaries containing `chain_id`, `chain_name`, `chain_type`. |
| **`"bonds"`** | List of Dicts | Covalent bond dictionaries specifying `atom1_index`, `atom2_index`, `bond_id`, `bond_order`, `is_aromatic`. |

---

## Usage and Workflow

```python
import molsysmt as msm

# 1. Convert native Topology to TopologyDict
top_dict = msm.convert(topology, to_form='molsysmt.TopologyDict')

# 2. Extract primitive dictionary data
data = top_dict.to_dict()
```

---

## Invariants and Performance

- **JSON Compatibility**: Pure Python primitives (`dict`, `list`, `str`, `int`) for straightforward JSON transport.
- **Deep Copy Isolation**: `top_dict.to_dict(copy=True)` returns isolated dictionary copies.

---

## API Documentation

Detailed methods for `molsysmt.TopologyDict` are documented in the [{doc}`molsysmt.Topology API Reference </api/form/molsysmt_Topology/api_molsysmt_Topology>`].
