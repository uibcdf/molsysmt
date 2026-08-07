(user-foundations-native-world-classes-molsysmt-topology)=
# Topology

`molsysmt.Topology` is the native data structure in MolSysMT responsible for managing atom inventories, residue groups, molecular entities, chemical chains, and covalent bonding graphs.

---

## Overview

As a user, `molsysmt.Topology` is the object holding all structural identity and chemical metadata for a system. It provides fast selection queries, atom index resolution, and structural hierarchy traversals without needing 3D spatial coordinates.

---

## Attributes

Inside `molsysmt.Topology`, data is maintained across optimized tabular attributes:

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| **`atoms`** | NumPy structured array | Atom inventory storing atom names, atom types, element symbols, and string IDs. |
| **`groups`** | NumPy structured array | Group/residue inventory holding group names, residue numbers, and group types. |
| **`components`** | NumPy structured array | Connected chemical graph components. |
| **`molecules`** | NumPy structured array | Higher-level biological molecule classifications. |
| **`chains`** | NumPy structured array | Structural chain identifiers and segment labels. |
| **`bonds`** | NumPy structured array | Covalent bond graph specifying atom index pairs, bond order, and aromaticity. |

---

## Invariants

- **String Identifier Invariant**: Atom IDs, group IDs, and chain IDs are strictly normalized to string representations.
- **Fast Selections**: Optimized for zero-overhead Boolean evaluation by MolSysMT's internal selection parser.

---

## API Reference

All methods, getters, and converters for `molsysmt.Topology` are documented in the [{doc}`molsysmt.Topology API Reference </api/form/molsysmt_Topology/api_molsysmt_Topology>`].
