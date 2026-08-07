(user-foundations-native-world-classes-molsysmt-molecularmechanics)=
# molsysmt.MolecularMechanics

`molsysmt.MolecularMechanics` is the native data container in MolSysMT responsible for managing force field parameters, partial atomic charges, atomic masses, and non-bonded interaction settings.

---

## Conceptual Overview & User Role

As a user, `molsysmt.MolecularMechanics` is the object holding physical mechanics parameters required for energy evaluations, molecular dynamics simulations, or electrostatics calculations.

---

## Internal Architecture & Attributes (What's Inside)

Inside `molsysmt.MolecularMechanics`, parameters are stored as attribute arrays bound to physical units:

| Attribute | Data Type | Physical Units | Description |
| :--- | :--- | :--- | :--- |
| **`forcefield`** | String | N/A | Name of the assigned forcefield (e.g. `'AMBER14'`, `'CHARMM36'`). |
| **`charge`** | NumPy `float64` array | `elementary charge` (`e`) | Partial atomic charges for each atom `(n_atoms,)`. |
| **`mass`** | NumPy `float64` array | `dalton` (`Da`) | Atomic masses for each atom `(n_atoms,)`. |
| **`non_bonded_method`** | String | N/A | Non-bonded interaction method (e.g. `'PME'`, `'NoCutoff'`). |

---

## Declarative Serialization (`MolecularMechanicsDict`)

`molsysmt.MolecularMechanics` instances convert seamlessly to and from declarative Python dictionaries (`molsysmt.MolecularMechanicsDict`):

```python
import molsysmt as msm

# 1. Extract MolecularMechanics from system
mm = msm.get(system, element='system', molecular_mechanics=True)

# 2. Convert to MolecularMechanicsDict
mm_dict = mm.to_dict()

# 3. Reconstruct MolecularMechanics from dictionary
new_mm = msm.convert(mm_dict, to_form='molsysmt.MolecularMechanics')
```

---

## Invariants, Performance & API Reference

- **Float64 Precision**: Charges and masses use double-precision `float64` for numerical accuracy during energy evaluation.
- **API Reference**: Detailed methods and converters for `molsysmt.MolecularMechanics` are documented in the [{doc}`molsysmt.MolecularMechanics API Reference </api/form/molsysmt_MolecularMechanics/api_molsysmt_MolecularMechanics>`].
