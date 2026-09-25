(user-foundations-native-world-classes-molsysmt-molsysbuilder)=
# MolSysBuilder

`molsysmt.MolSysBuilder` is the native editable staging container in MolSysMT designed for incremental system assembly, structural editing, and model modifications.

---

## Overview and Role

While `molsysmt.MolSys` is an immutable state container optimized for fast computation, `molsysmt.MolSysBuilder` provides an active, mutable staging environment. It allows users to incrementally declare atoms, group residues, specify covalent bonds, assign 3D coordinates, and validate system integrity before compiling back into a production `molsysmt.MolSys` object.

For most users and workflows, the recommended entry point to create and work with an editable builder is the {func}`molsysmt.build.editable` tool (see the {ref}`Editable Tutorial <Tutorial_Editable>`). Calling `msm.build.editable(molsys)` converts any supported molecular system format into an active `MolSysBuilder` instance ready for editing, while calling `msm.build.editable()` without arguments initializes an empty builder from scratch.

Under the hood, `MolSysBuilder` manages staging instances of native `Topology` and `Structures` containers, enabling standard query functions like `msm.get()` and `msm.info()` to inspect uncompiled staging models directly.

---

## Internal Staging Tables

Inside `molsysmt.MolSysBuilder`, staging data is organized across internal topological data frames and structural coordinate buffers:

| Internal Staging Attribute | Data Class / Type | Description |
| :--- | :--- | :--- |
| **`topology`** | `molsysmt.Topology` | Mutable topological graph storing staging DataFrames for `atoms`, `groups`, `components`, `molecules`, `entities`, `chains`, and `bonds`. |
| **`structures`** | `molsysmt.Structures` | Mutable spatial container holding coordinate buffers `(n_structures, n_atoms, 3)`, periodic box matrices `(n_structures, 3, 3)`, and timestamps. |

---

## Working with a MolSysBuilder

A `MolSysBuilder` supports two primary operational workflows: editing existing molecular systems or assembling new models from scratch.

### Editing Existing Systems

Any supported molecular system can be made editable to modify bonds, reassign chains, or alter topological groupings:

```python
import molsysmt as msm

# 1. Convert an existing system into an editable builder
builder = msm.build.editable(molsys)

# 2. Modify topological attributes and bonds
builder.add_bond(atom_index_1=0, atom_index_2=10, bond_order=1, bond_type='covalent')
builder.assign_groups_to_new_chain(group_indices=[0, 1], chain_id='B', chain_name='B')

# 3. Validate and compile into a production MolSys instance
new_molsys = builder.build()
```

### Assembling Systems from Scratch

An empty builder can incrementally construct complete systems atom by atom, residue by residue, and structure by structure:

```python
import numpy as np
import molsysmt as msm

# 1. Initialize an empty builder
builder = msm.build.editable()

# 2. Incrementally declare atoms, residues, chains, and bonds
builder.add_atom(atom_name='N', atom_type='N')
builder.add_atom(atom_name='CA', atom_type='C')
builder.add_atom(atom_name='C', atom_type='C')
builder.add_group(atom_indices=[0, 1, 2], group_name='ALA', group_id='1', group_type='amino_acid')
builder.add_chain(group_indices=[0], chain_id='A', chain_name='A')
builder.add_bond(atom_index_1=0, atom_index_2=1, bond_order=1, bond_type='covalent')
builder.add_bond(atom_index_1=1, atom_index_2=2, bond_order=1, bond_type='covalent')

# 3. Assign structural coordinates and box dimensions
coords = np.array([[[0.0, 0.0, 0.0], [0.145, 0.0, 0.0], [0.245, 0.12, 0.0]]]) * msm.pyunitwizard.unit('nm')
builder.set_coordinates(coords)

# 4. Validate and compile into a final immutable MolSys instance
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
