(user-foundations-native-world-classes-molsysmt-molsysbuilder)=
# MolSysBuilder

`molsysmt.MolSysBuilder` is the native editable staging container in MolSysMT designed for incremental system assembly, structural editing, and model modifications.

---

## Overview and Role

While `molsysmt.MolSys` is an immutable state container, `molsysmt.MolSysBuilder` provides an active, mutable staging environment. It allows users to incrementally declare atoms, group residues, specify covalent bonds, append 3D coordinates, and validate system integrity before compiling back into a production `molsysmt.MolSys` object.

Under the hood, `MolSysBuilder` manages staging instances of native `Topology` and `Structures` containers, enabling functions like `msm.get()` and `msm.info()` to query uncompiled staging models directly.

---

## Internal Staging Tables

Inside `molsysmt.MolSysBuilder`, staging data is organized across internal topological data frames and structural coordinate buffers:

| Internal Staging Attribute | Data Class / Type | Description |
| :--- | :--- | :--- |
| **`topology`** | `molsysmt.Topology` | Mutable topological graph storing staging DataFrames for `atoms`, `groups`, `components`, `molecules`, `entities`, `chains`, and `bonds`. |
| **`structures`** | `molsysmt.Structures` | Mutable spatial container holding coordinate buffers `(n_structures, n_atoms, 3)`, periodic box matrices `(n_structures, 3, 3)`, and timestamps. |

---

## Staging Operations

`molsysmt.MolSysBuilder` provides explicit methods for building and validating molecular models:

```python
import molsysmt as msm

# 1. Initialize an empty builder
builder = msm.MolSysBuilder()

# 2. Incrementally declare atoms and residues
atom1 = builder.add_atom(atom_name='N', atom_type='N')
atom2 = builder.add_atom(atom_name='CA', atom_type='C')
group1 = builder.add_group(atom_indices=[atom1, atom2], group_name='ALA', group_type='amino_acid')

# 3. Declare covalent bonds
builder.add_bond(atom_index_1=atom1, atom_index_2=atom2, bond_order=1, bond_type='covalent')

# 4. Validate and compile final immutable MolSys instance
system = builder.build()
```

---

## Invariants and Performance

- **Validation Checkpoint**: Calling `builder.build()` automatically verifies structural consistency (e.g. coordinates shape matching atom counts, non-empty group memberships).
- **Atom Editing Lock**: Atom addition is locked once structural coordinate arrays have been assigned to prevent shape mismatch corruption.
- **String Identifier Invariant**: Incoming numeric IDs are automatically normalized to string representations.

---

## API Documentation

Detailed methods for `molsysmt.MolSysBuilder` are documented in the [{doc}`molsysmt.MolSysBuilder API Reference </api/form/molsysmt_MolSys/api_molsysmt_MolSys>`].
