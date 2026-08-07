(user-foundations-native-world-classes-molsysmt-structures)=
# molsysmt.Structures

`molsysmt.Structures` is the native data container in MolSysMT designed for storing 3D atomic coordinates, periodic box vectors, and frame timestamps across trajectory structure sequences.

---

## Conceptual Overview & User Role

As a user, `molsysmt.Structures` is the object holding all geometric and spatial trajectory data. It manages 3D coordinate arrays, unit cell box vectors, and frame timestamps across single structures or multi-frame trajectories.

---

## Internal Architecture & Attributes (What's Inside)

Inside `molsysmt.Structures`, spatial data is stored as C-contiguous NumPy arrays bound to physical units:

| Attribute | Data Type | Physical Units | Dimensions / Shape | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`coordinates`** | NumPy `float32` array | `nanometers` (`nm`) | `(n_structures, n_atoms, 3)` | 3D Cartesian coordinates for each frame and atom. |
| **`box`** | NumPy `float32` array | `nanometers` (`nm`) | `(n_structures, 3, 3)` | Periodic unit cell vectors for each frame. |
| **`time`** | NumPy `float64` array | `picoseconds` (`ps`) | `(n_structures,)` | Simulation time or frame timestamps. |
| **`structure_id`** | List of Strings | N/A | `(n_structures,)` | String identifiers for structural frames or PDB models. |

---

## Declarative Serialization (`StructuresDict`)

`molsysmt.Structures` instances convert seamlessly to and from declarative Python dictionaries (`molsysmt.StructuresDict`):

```python
import molsysmt as msm

# 1. Extract Structures from system
structures = msm.get(system, element='system', structures=True)

# 2. Convert to StructuresDict
struct_dict = structures.to_dict()

# 3. Reconstruct Structures from dictionary
new_structures = msm.convert(struct_dict, to_form='molsysmt.Structures')
```

---

## Invariants, Performance & API Reference

- **Zero-Copy Views**: Slicing structures returns zero-copy NumPy array views whenever possible.
- **Float32 Precision**: Coordinates default to `float32` for optimal memory footprint and GPU hardware acceleration.
- **API Reference**: Detailed methods, getters, and converters for `molsysmt.Structures` are documented in the [{doc}`molsysmt.Structures API Reference </api/form/molsysmt_Structures/api_molsysmt_Structures>`].
