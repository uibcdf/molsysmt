(user-foundations-native-world-classes-molsysmt-structures)=
# Structures

`molsysmt.Structures` is the native data container in MolSysMT designed for storing 3D atomic coordinates, periodic box vectors, and frame timestamps across structure sequences.

---

## Overview

As a user, `molsysmt.Structures` is the object holding all geometric and spatial data. It manages 3D coordinate arrays, unit cell box vectors, and frame timestamps across single structures or multi-frame structure ensembles.

---

## Attributes

Inside `molsysmt.Structures`, spatial data is stored as C-contiguous NumPy arrays:

| Attribute | Data Type | Dimensions / Shape | Description |
| :--- | :--- | :--- | :--- |
| **`coordinates`** | NumPy `float32` array | `(n_structures, n_atoms, 3)` | 3D Cartesian coordinates (in `nm`). |
| **`box`** | NumPy `float32` array | `(n_structures, 3, 3)` | Periodic unit cell vectors (in `nm`). |
| **`time`** | NumPy `float64` array | `(n_structures,)` | Frame timestamps (in `ps`). |
| **`structure_id`** | List of Strings | `(n_structures,)` | String identifiers for structural frames or PDB models. |

---

## Invariants

- **Zero-Copy Views**: Slicing structures returns zero-copy NumPy array views whenever possible.
- **Float32 Precision**: Coordinates default to `float32` for optimal memory footprint and hardware acceleration.

---

## API Reference

Detailed methods, getters, and converters for `molsysmt.Structures` are documented in the [{doc}`molsysmt.Structures API Reference </api/form/molsysmt_Structures/api_molsysmt_Structures>`].
