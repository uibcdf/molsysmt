(user-foundations-native-world-classes-molsysmt-molsysbuilder)=
# molsysmt.MolSysBuilder

`molsysmt.MolSysBuilder` is the native editable staging container in MolSysMT designed for incremental system assembly, structural editing, and model modifications.

---

## Conceptual Overview & User Role

While `molsysmt.MolSys` is an immutable state container, `molsysmt.MolSysBuilder` provides a mutable staging area where users can incrementally add, remove, reorder, or mutate atoms, residues, molecules, coordinates, and forcefield terms.

Once staging modifications are complete, the builder validates topological integrity and compiles the staged tables into a production-ready `molsysmt.MolSys` object.

---

## Internal Architecture & Staging Tables (What's Inside)

Inside `molsysmt.MolSysBuilder`, molecular components are stored as dynamic tabular data frames:

| Staging Component | Internal Representation | Description |
| :--- | :--- | :--- |
| **`atoms_table`** | Dynamic Pandas/Arrow DataFrame | Mutable atom inventory containing names, types, element symbols, and string IDs. |
| **`groups_table`** | Dynamic Pandas/Arrow DataFrame | Group and residue definitions, sequence numbers, and group types (amino acid, water, ion). |
| **`components_table`** | Dynamic Data Table | Connected molecular graph components. |
| **`molecules_table`** | Dynamic Data Table | Higher-level biological molecule entities (proteins, nucleic acids, solvents). |
| **`chains_table`** | Dynamic Data Table | Chain identifiers and structural segment groupings. |
| **`bonds_table`** | Dynamic Bond List | Covalent bond inventory with order and aromaticity flags. |
| **`coordinates_buffer`** | Dynamic NumPy array list | Mutable 3D spatial coordinates in nanometers. |

---

## Staging Operations & Compilation Workflow

`molsysmt.MolSysBuilder` provides specialized methods for incremental model construction:

```python
import molsysmt as msm

# 1. Initialize an empty builder
builder = msm.MolSysBuilder()

# 2. Incrementally append atoms, residues, or external system fragments
builder.add_group(name='ALA', group_type='amino_acid')
builder.add_atom(name='CA', atom_type='C', element='C')

# 3. Build and validate final immutable MolSys instance
system = builder.build()
```

---

## Invariants, Performance & API Reference

- **Validation Checkpoint**: `builder.build()` automatically validates topological invariants (unique atom indices, non-empty groups, valid coordinate dimensions) before compiling.
- **String Identifier Invariant**: Incoming numeric IDs are automatically converted and normalized to string representations.
- **API Reference**: Detailed methods for `molsysmt.MolSysBuilder` are documented in the [{doc}`molsysmt.MolSysBuilder API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].
