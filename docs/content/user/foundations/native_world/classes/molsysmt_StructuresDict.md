(user-foundations-native-world-classes-molsysmt-structuresdict)=
# StructuresDict

`molsysmt.StructuresDict` is the native declarative dictionary representation of structural and trajectory data in MolSysMT.

---

## Overview and Role

`molsysmt.StructuresDict` provides a JSON-compatible dictionary schema representing 3D Cartesian atomic coordinates, periodic cell box matrices, frame timestamps, velocities, and thermodynamic observables.

---

## Declarative Schema

The schema dictionary maps standard structure parameters to nested list arrays or base64 binary encodings:

| Top-Level Key | Value Type | Physical Units | Description |
| :--- | :--- | :--- | :--- |
| **`"coordinates"`** | Nested List or Base64 | `nanometer` (`nm`) | 3D Cartesian coordinates array `(n_structures, n_atoms, 3)`. |
| **`"velocities"`** | Nested List or Base64 | `nm / ps` | Atomic velocity vectors `(n_structures, n_atoms, 3)`. |
| **`"box"`** | Nested List | `nanometer` (`nm`) | Periodic unit cell box matrices `(n_structures, 3, 3)`. |
| **`"time"`** | Nested List | `picosecond` (`ps`) | Frame timestamps array `(n_structures,)`. |
| **`"structure_id"`** | List of Strings | N/A | String identifiers for structural frames or PDB models. |
| **`"b_factor"`** | Nested List | `nm²` | Crystallographic B-factors `(n_structures, n_atoms)`. |
| **`"occupancy"`** | Nested List | Dimensionless | Crystallographic atom occupancy values `(n_structures, n_atoms)`. |
| **`"alternate_location"`** | List of Dicts | N/A | Alternate location mapping dicts. |
| **`"temperature"`** | Nested List | `kelvin` (`K`) | Frame-level temperatures `(n_structures,)`. |
| **`"potential_energy"`** | Nested List | `kJ / mol` | Frame-level potential energies `(n_structures,)`. |
| **`"kinetic_energy"`** | Nested List | `kJ / mol` | Frame-level kinetic energies `(n_structures,)`. |

---

## Usage and Workflow

```python
import molsysmt as msm

# Convert native Structures container to StructuresDict
struct_dict = msm.convert(structures, to_form='molsysmt.StructuresDict')
```

---

## Invariants and Performance

- **JSON Encodable**: Encodable into standard JSON string representations.

---

## API Documentation

Methods for `molsysmt.StructuresDict` are documented in the [{doc}`molsysmt.Structures API Reference </api/form/molsysmt_Structures/api_molsysmt_Structures>`].
