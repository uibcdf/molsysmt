(user-foundations-native-world-classes-molsysmt-molecularmechanics)=
# MolecularMechanics

`molsysmt.MolecularMechanics` is the native data container in MolSysMT responsible for managing force field parameters, partial atomic charges, atomic masses, and non-bonded interaction settings.

---

## Overview

As a user, `molsysmt.MolecularMechanics` is the object holding physical mechanics parameters required for energy evaluations, molecular dynamics simulations, or electrostatics calculations.

---

## Attributes

Inside `molsysmt.MolecularMechanics`, parameters are stored as attribute arrays:

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| **`forcefield`** | String | Name of the assigned forcefield (e.g. `'AMBER14'`, `'CHARMM36'`). |
| **`charge`** | NumPy `float64` array | Partial atomic charges for each atom `(n_atoms,)` in elementary charge `e`. |
| **`mass`** | NumPy `float64` array | Atomic masses for each atom `(n_atoms,)` in `Da`. |
| **`non_bonded_method`** | String | Non-bonded interaction method (e.g. `'PME'`, `'NoCutoff'`). |

---

## Invariants

- **Float64 Precision**: Charges and masses use double-precision `float64` for numerical accuracy during energy evaluation.

---

## API Reference

Detailed methods and converters for `molsysmt.MolecularMechanics` are documented in the [{doc}`molsysmt.MolecularMechanics API Reference </api/form/molsysmt_MolecularMechanics/api_molsysmt_MolecularMechanics>`].
