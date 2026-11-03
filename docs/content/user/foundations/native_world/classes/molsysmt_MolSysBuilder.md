(user-foundations-native-world-classes-molsysmt-molsysbuilder)=
# MolSysBuilder

`molsysmt.MolSysBuilder` is the native editable staging container in MolSysMT designed for incremental system assembly, structural editing, and model modifications.

---

## Overview and Role

`MolSys` coordinates molecular domains for computation and analysis. `MolSysBuilder`
stages incremental declarations: atoms, groups, covalent bonds and 3D structures
can be assembled and validated before producing a `MolSys`.

For most users and workflows, the recommended entry point to create and work with an editable builder is the {func}`molsysmt.build.editable` tool (see the {ref}`Editable Tutorial <Tutorial_Editable>`). Calling `msm.build.editable(molsys)` converts a supported molecular system with a stable topology into an active `MolSysBuilder` instance ready for editing, while calling `msm.build.editable()` without arguments initializes an empty builder from scratch.

`MolSysBuilder` manages separate native inventory, chemical and structural
staging domains. Standard query functions like `msm.get()` and `msm.info()`
can inspect uncompiled staging models directly.

---

## Internal Staging Tables

`builder.copy()` and Python `copy.deepcopy(builder)` copy staging data eagerly.
`builder.copy(deep=False)` and Python `copy.copy(builder)` share protected
coordinate/box blocks through independent handles. Staging tables, other series
and metadata detach in both modes. Copying does not call `build()`, invent missing
groups/parents or normalize incomplete declarations. Counts read stored axis
metadata without assembling coordinates. See
{ref}`Native Copying <user-foundations-resident-copying>`.

Inside `molsysmt.MolSysBuilder`, staging data is organized across independent domain tables and structural coordinate buffers:

| Internal Staging Attribute | Data Class / Type | Description |
| :--- | :--- | :--- |
| **`topology`** | `molsysmt.Topology` | Stable inventory tables for `atoms`, `groups`, `molecules`, `entities` and `chains`. It has no bond or component facade. |
| **`chemical_states`** | `molsysmt.ChemicalStates` or `None` | State-local bonds, chemical assignments and components. Missing chemistry remains unavailable; an existing collection with zero states stays empty. |
| **`structures`** | `molsysmt.Structures` | Spatial staging for coordinates `(n_structures, n_atoms, 3)` and periodic boxes `(n_structures, 3, 3)` in nm, and time in ps. A source without structures receives an empty container without observations. |

Staging retains all existing chemical states, their labels, reference selection
and preparation history. Bond edits act on the resolved state; an ambiguous
multi-state collection requires `chemical_state=` explicitly. Reading
`builder.n_bonds` or editing bonds when chemistry is absent or has no states
raises a structural prerequisite error. Creating the builder does not infer
bonds or create a state to satisfy that query. Named interaction analyses and
molecular mechanics are outside the builder's stored domains.

---

## Working with a MolSysBuilder

A `MolSysBuilder` supports two primary operational workflows: editing existing molecular systems or assembling new models from scratch.

### Editing Existing Systems

A supported molecular system with a stable topology can be made editable to
modify declared bonds, reassign chains, or alter inventory groupings:

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

### Missing Domains

A stable topology is required for editing. A system containing only structures
or chemical states raises a structural prerequisite error; supply its stable
inventory explicitly first. A missing structural domain is different: staging
can start without coordinates. Absent chemistry stays absent after building,
and the input system remains unchanged:

```python
import molsysmt as msm
from molsysmt.native import Topology

molsys = msm.convert(Topology(n_atoms=2), to_form='molsysmt.MolSys')
molsys.structures = None
builder = msm.build.editable(molsys)
assert builder.n_structures == 0
assert builder.chemical_states is None
new_molsys = builder.build()
assert new_molsys.chemical_states is None
assert new_molsys.structures.coordinates is None
assert molsys.structures is None
```

### Assembling Systems from Scratch

An empty builder can incrementally construct complete systems atom by atom,
group by group, and structure by structure:

```python
import numpy as np
import molsysmt as msm

# 1. Initialize an empty builder
builder = msm.build.editable()

# 2. Incrementally declare atoms, groups, chains, and bonds
builder.add_atom(atom_name='N', atom_type='N')
builder.add_atom(atom_name='CA', atom_type='C')
builder.add_atom(atom_name='C', atom_type='C')
builder.add_group(atom_indices=[0, 1, 2], group_name='ALA', group_id='1', group_type='amino acid')
builder.add_chain(group_indices=[0], chain_id='A', chain_name='A')
builder.add_bond(atom_index_1=0, atom_index_2=1, bond_order=1, bond_type='covalent')
builder.add_bond(atom_index_1=1, atom_index_2=2, bond_order=1, bond_type='covalent')

# 3. Assign structural coordinates and box dimensions
coords = np.array([[[0.0, 0.0, 0.0], [0.145, 0.0, 0.0], [0.245, 0.12, 0.0]]]) * msm.pyunitwizard.unit('nm')
builder.set_coordinates(coords)

# 4. Validate and compile into a MolSys instance
molsys = builder.build()
```

---

## Invariants and Performance

- **Validation Checkpoint**: Calling `builder.build()` automatically verifies structural consistency (e.g. coordinates shape matching atom counts, non-empty group memberships).
- **Atom Editing Lock**: Atom addition is locked once structural coordinate arrays have been assigned to prevent shape mismatch corruption.
- **String Identifier Invariant**: Incoming numeric IDs are automatically normalized to string representations.

---

## API Documentation

See {ref}`API Native Queries` for resident-object queries and
{func}`molsysmt.basic.convert` for form-agnostic conversion.

## Native Queries

Inspect the current staging data with `builder.get(...)` and `builder.info(...)` without finalizing a system. Both methods validate options by default, including attribute flags and skip_digestion; new atoms are visible to later queries. Native `info()` supports Styler, DataFrame and dictionary records. See {ref}`Tutorial_Get` and {ref}`Tutorial_Info`.

## Inherited Molecules

Adding groups to a group-free source preserves its molecule indices, string IDs,
names and types. Partially grouped sources receive fallback groups for remaining
atoms during build, with the same inherited ownership. Groups spanning different
inherited molecules are rejected before insertion. New builders without an
inherited axis retain ordinary inference. Staging keeps a compact source-atom
ownership map; it does not create a second chemical store. The source system
remains unchanged. See {ref}`Cookbook_Group_Free_Hierarchy` for executed examples.

## Atom Inventory

Appending an atom extends every chemical state with aligned nullable rows. Old
assignments, bonds, state labels, reference selection and original producer
history are retained. The new atom has unknown chemical assignments; no formal
charge, aromaticity, valence or hydrogen inventory is guessed. Complete
connectivity/component declarations become partial, so scientific readers can
require explicit chemical completion before evaluating the result.

Atom metadata and all extended state tables are prepared and validated before
publication. Validation/allocation failure leaves the staging inventory unchanged.
The strict post-edit alignment validator remains active. Existing coordinates,
velocities or B factors prohibit adding atoms; structural arrays are not silently
resized. State bonds/components and coordinate series are not copied by atom
growth itself. This does not establish a concurrent-edit transaction or introduce
another chemical store. See {ref}`Cookbook_Group_Free_Hierarchy` for an executed
append/group/build workflow.

Group-free compilation keeps the missing group axis while extending molecule
metadata for new disconnected components. Inherited molecule positions and labels
remain aligned even for a permuted source. A connectivity edit that splits or
merges state-local components does not redefine inherited molecule membership,
including when there are no groups.

## Group Inventories

`add_group([], ...)` can declare a group before any atoms exist. `add_chain`
accepts ordered group indices and also an empty list for a declared empty chain.
Generated chain IDs follow `A` through `Z`, then `AA`, `AB`, and onward;
explicit IDs are preserved. `build()` retains these groups and chain memberships,
fills missing hierarchy metadata from local declarations and leaves atomic
connectivity unavailable. It does not create representative atoms or a chemical
realization. Known group types and molecule occurrences survive compilation.
