(user-foundations-native-world-classes-molsysmt-structuresdict)=
# StructuresDict

`molsysmt.StructuresDict` is the native declarative dictionary representation of structural data in MolSysMT.

---

## Overview and Role

`molsysmt.StructuresDict` provides a JSON-compatible dictionary schema representing 3D atomic coordinates, periodic box matrices, and frame timestamps.

---

## Declarative Schema

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"coordinates"`** | Nested List or Base64 | Cartesian coordinate array data (in `nm`). |
| **`"box"`** | Nested List | Periodic unit cell box matrices `(n_structures, 3, 3)` (in `nm`). |
| **`"time"`** | Nested List | Frame timestamps (in `ps`). |

---

## Usage and Workflow

```python
import molsysmt as msm

# Convert native Structures to StructuresDict
struct_dict = msm.convert(structures, to_form='molsysmt.StructuresDict')
```

---

## Invariants and Performance

- **JSON Compatibility**: Convertible to pure JSON data strings.

---

## API Documentation

Methods for `molsysmt.StructuresDict` are documented in the [{doc}`molsysmt.Structures API Reference </api/form/molsysmt_Structures/api_molsysmt_Structures>`].
