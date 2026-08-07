(user-foundations-native-world-classes-molsysmt-topology)=
# molsysmt.Topology

`molsysmt.Topology` is the native data structure in MolSysMT responsible for managing atom inventories, residue groups, molecular entities, chemical chains, and covalent bonding graphs.

---

## Conceptual Overview & User Role

As a user, `molsysmt.Topology` is the object holding all structural identity and chemical metadata for a system. It provides fast selection queries, atom index resolution, and structural hierarchy traversals without needing 3D spatial coordinates.

---

## Internal Architecture & Attributes (What's Inside)

Inside `molsysmt.Topology`, data is maintained across optimized tabular attributes:

| Attribute | Data Type | Physical Units | Description |
| :--- | :--- | :--- | :--- |
| **`atoms`** | NumPy structured array | N/A | Atom inventory storing atom names, atom types, element symbols, and string IDs. |
| **`groups`** | NumPy structured array | N/A | Group/residue inventory holding group names, residue numbers, and group types. |
| **`components`** | NumPy structured array | N/A | Connected chemical graph components. |
| **`molecules`** | NumPy structured array | N/A | Higher-level biological molecule classifications. |
| **`chains`** | NumPy structured array | N/A | Structural chain identifiers and segment labels. |
| **`bonds`** | NumPy structured array | N/A | Covalent bond graph specifying atom index pairs, bond order, and aromaticity. |

---

## Declarative Serialization (`TopologyDict`)

`molsysmt.Topology` instances can be converted to and from declarative Python dictionaries (`molsysmt.TopologyDict`):

```python
import molsysmt as msm

# 1. Extract Topology from system
topology = msm.get(system, element='system', topology=True)

# 2. Convert to TopologyDict
top_dict = topology.to_dict()

# 3. Reconstruct Topology from dictionary
new_topology = msm.convert(top_dict, to_form='molsysmt.Topology')
```

---

## Invariants, Performance & API Reference

- **String Identifier Invariant**: Atom IDs, group IDs, and chain IDs are strictly normalized to string representations.
- **Fast Selections**: Optimized for zero-overhead Boolean evaluation by MolSysMT's internal selection parser.
- **API Reference**: All methods, getters, and converters for `molsysmt.Topology` are documented in the [{doc}`molsysmt.Topology API Reference </api/form/molsysmt_Topology/api_molsysmt_Topology>`].
