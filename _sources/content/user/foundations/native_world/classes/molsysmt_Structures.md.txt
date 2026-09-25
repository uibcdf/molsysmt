(user-foundations-native-world-classes-molsysmt-structures)=
# Structures

`molsysmt.Structures` is the native data container in MolSysMT designed for storing 3D atomic coordinates, periodic box vectors, frame timestamps, and physical trajectory observables.

---

## Overview and Role

As a user, `molsysmt.Structures` is the object holding all geometric and spatial data. It manages 3D coordinate arrays, unit cell box vectors, frame timestamps, velocities, and thermodynamic observables across single structures or multi-frame structure ensembles.

---

## Internal Attributes

Inside `molsysmt.Structures`, spatial and thermodynamic observables are stored as C-contiguous NumPy arrays or attribute lists:

| Attribute | Data Type | Physical Units | Dimensions / Shape | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`coordinates`** | NumPy `float32` array | `nanometer` (`nm`) | `(n_structures, n_atoms, 3)` | 3D Cartesian coordinates for each frame and atom. |
| **`velocities`** | NumPy `float32` array | `nm / ps` | `(n_structures, n_atoms, 3)` | Atomic velocity vectors for each frame and atom. |
| **`box`** | NumPy `float32` array | `nanometer` (`nm`) | `(n_structures, 3, 3)` | Periodic unit cell vectors for each frame. |
| **`time`** | NumPy `float64` array | `picosecond` (`ps`) | `(n_structures,)` | Simulation timestamps for each structural frame. |
| **`structure_id`** | List of Strings | N/A | `(n_structures,)` | String identifiers for structural frames or PDB models. |
| **`b_factor`** | NumPy `float32` array | `nm²` | `(n_structures, n_atoms)` | Isotropic temperature factors (B-factors). |
| **`occupancy`** | NumPy `float32` array | Dimensionless | `(n_structures, n_atoms)` | Crystallographic atom occupancy values. |
| **`alternate_location`** | List of Dicts | N/A | `(n_structures,)` | Alternate location indicators mapping atom indices to location keys. |
| **`temperature`** | NumPy `float64` array | `kelvin` (`K`) | `(n_structures,)` | Frame-level system temperature. |
| **`potential_energy`** | NumPy `float64` array | `kJ / mol` | `(n_structures,)` | Frame-level potential energy. |
| **`kinetic_energy`** | NumPy `float64` array | `kJ / mol` | `(n_structures,)` | Frame-level kinetic energy. |

---

## Invariants and Performance

- **Zero-Copy Views**: Slicing structures returns zero-copy NumPy array views whenever possible.
- **Float32 Precision Default**: Coordinates and velocities default to `float32` for optimal memory footprint and GPU hardware acceleration.
- **Float64 Precision for Energies**: Thermodynamic observables (`temperature`, `potential_energy`, `kinetic_energy`, `time`) use double-precision `float64`.

---

## API Documentation

Detailed methods, getters, and converters for `molsysmt.Structures` are documented in the [{doc}`molsysmt.Structures API Reference </api/form/molsysmt_Structures/api_molsysmt_Structures>`].
