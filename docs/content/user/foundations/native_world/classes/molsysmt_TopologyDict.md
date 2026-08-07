(user-foundations-native-world-classes-molsysmt-topologydict)=
# molsysmt.TopologyDict

`molsysmt.TopologyDict` is the native declarative dictionary representation of molecular topology in MolSysMT.

---

## Conceptual Overview & User Role

`molsysmt.TopologyDict` provides a lightweight, JSON-serializable dictionary schema representing atoms, residues, molecules, chains, and bonds.

---

## Internal Dictionary Schema (What's Inside)

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"atoms"`** | List of Dicts | Atom dictionaries containing `"name"`, `"type"`, `"element"`, and `"id"`. |
| **`"groups"`** | List of Dicts | Residue dictionaries containing `"name"`, `"number"`, and `"group_type"`. |
| **`"chains"`** | List of Dicts | Chain dictionaries containing `"id"` and `"name"`. |
| **`"bonds"`** | List of Dicts | Covalent bond dictionary list specifying `"atom1_index"`, `"atom2_index"`, and `"order"`. |

---

## Usage Example

```python
import molsysmt as msm

# Convert native Topology to TopologyDict
top_dict = msm.convert(topology, to_form='molsysmt.TopologyDict')
```

---

## Invariants, Performance & API Reference

- **JSON Compatibility**: Pure Python primitives suitable for direct JSON serialization.
- **API Reference**: Detailed methods for `molsysmt.TopologyDict` are documented in the [{doc}`molsysmt.Topology API Reference </api/form/molsysmt_Topology/api_molsysmt_Topology>`].
