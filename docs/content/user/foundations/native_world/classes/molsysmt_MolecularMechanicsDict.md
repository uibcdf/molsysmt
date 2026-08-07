(user-foundations-native-world-classes-molsysmt-molecularmechanicsdict)=
# molsysmt.MolecularMechanicsDict

`molsysmt.MolecularMechanicsDict` is the native declarative dictionary representation of molecular mechanics parameters in MolSysMT.

---

## Conceptual Overview & User Role

`molsysmt.MolecularMechanicsDict` provides a JSON-compatible dictionary schema representing forcefield names, atomic partial charges, and atomic masses.

---

## Internal Dictionary Schema (What's Inside)

| Top-Level Key | Value Type | Physical Units | Description |
| :--- | :--- | :--- | :--- |
| **`"forcefield"`** | String | N/A | Forcefield identifier string. |
| **`"charge"`** | Nested List | `e` | Partial charges list. |
| **`"mass"`** | Nested List | `Da` | Atomic masses list. |

---

## Usage Example

```python
import molsysmt as msm

# Convert native MolecularMechanics to MolecularMechanicsDict
mm_dict = msm.convert(mm, to_form='molsysmt.MolecularMechanicsDict')
```

---

## Invariants, Performance & API Reference

- **JSON Compatibility**: Pure Python primitives for JSON transport.
- **API Reference**: Detailed methods for `molsysmt.MolecularMechanicsDict` are documented in the [{doc}`molsysmt.MolecularMechanics API Reference </api/form/molsysmt_MolecularMechanics/api_molsysmt_MolecularMechanics>`].
