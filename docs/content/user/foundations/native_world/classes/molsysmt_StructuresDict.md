(user-foundations-native-world-classes-molsysmt-structuresdict)=
# molsysmt.StructuresDict

`molsysmt.StructuresDict` is the native declarative dictionary representation of structural and trajectory data in MolSysMT.

---

## Conceptual Overview & User Role

`molsysmt.StructuresDict` provides a JSON-compatible dictionary schema representing 3D atomic coordinates, periodic box matrices, and frame timestamps.

---

## Internal Dictionary Schema (What's Inside)

| Top-Level Key | Value Type | Physical Units | Description |
| :--- | :--- | :--- | :--- |
| **`"coordinates"`** | Nested List or Base64 | `nm` | Cartesian coordinate array data. |
| **`"box"`** | Nested List | `nm` | Periodic unit cell box matrices `(n_structures, 3, 3)`. |
| **`"time"`** | Nested List | `ps` | Simulation time array. |

---

## Usage Example

```python
import molsysmt as msm

# Convert native Structures to StructuresDict
struct_dict = msm.convert(structures, to_form='molsysmt.StructuresDict')
```

---

## Invariants, Performance & API Reference

- **JSON Compatibility**: Convertible to pure JSON data strings.
- **API Reference**: Methods for `molsysmt.StructuresDict` are documented in the [{doc}`molsysmt.Structures API Reference </api/form/molsysmt_Structures/api_molsysmt_Structures>`].
