(user-foundations-native-world-classes-molsysmt-molecularmechanicsdict)=
# MolecularMechanicsDict

`molsysmt.MolecularMechanicsDict` is the native declarative dictionary representation of molecular mechanics parameters in MolSysMT.

---

## Overview

`molsysmt.MolecularMechanicsDict` provides a JSON-compatible dictionary schema representing forcefield names, atomic partial charges, and atomic masses.

---

## Schema

| Top-Level Key | Value Type | Description |
| :--- | :--- | :--- |
| **`"forcefield"`** | String | Forcefield identifier string. |
| **`"charge"`** | Nested List | Partial charges list in `e`. |
| **`"mass"`** | Nested List | Atomic masses list in `Da`. |

---

## Usage

```python
import molsysmt as msm

# Convert native MolecularMechanics to MolecularMechanicsDict
mm_dict = msm.convert(mm, to_form='molsysmt.MolecularMechanicsDict')
```

---

## Invariants

- **JSON Compatibility**: Pure Python primitives for JSON transport.

---

## API Reference

Detailed methods for `molsysmt.MolecularMechanicsDict` are documented in the [{doc}`molsysmt.MolecularMechanics API Reference </api/form/molsysmt_MolecularMechanics/api_molsysmt_MolecularMechanics>`].
