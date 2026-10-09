(user-foundations-native-world-classes-molsysmt-molecularmechanics)=
# MolecularMechanics

The native `MolecularMechanics` domain, accessed through `molsys.molecular_mechanics`,
holds prepared force-field parameters and non-bonded interaction settings.
It remains experimental; H5MSM 0.5 does not persist a nonempty mechanics domain.

---

## Overview and Role

As a user, `molsysmt.MolecularMechanics` is the object holding physical mechanics parameters required for energy evaluations, molecular dynamics simulations, or electrostatics calculations.

---

## Internal Attributes

Per-atom parameters share the row axis of the `atoms_ff` table. Scalar settings
are separate attributes:

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| **`forcefield`** | String | Name of the assigned forcefield (e.g. `'AMBER14'`, `'CHARMM36'`). |
| **`partial_charge`** | Numerical column | Partial atomic charges for each atom `(n_atoms,)` in elementary charge `e`. |
| **`atom_ff_type`** | Label column | Prepared force-field or parameter typing labels on the same atom axis. |
| **`partial_charge_assignment`**, **`atom_type_assignment`** | Optional reports | Original named-model provenance, cleared when the corresponding property is replaced. |
| **`non_bonded_method`** | String | Non-bonded interaction method (e.g. `'PME'`, `'NoCutoff'`). |

---

## Invariants and Performance

- Native charge values use elementary charge independently of the session's unit
  policy. Atom masses in `Da` are obtained through public atom attributes; they
  are not stored in this container.
- Merging concatenates prepared columns in input and selected atom order.
  Columns missing from a contributing input are cleared with a warning. Empty
  selections contribute nothing. Scalar settings come from the first input.
- Combining inputs or selecting atoms invalidates named assignment reports with
  a warning: the original reports do not describe the combined atom graph.
  A single full input retains detached reports. Input data are not modified.

---

## API Documentation

Detailed methods and converters for `molsysmt.MolecularMechanics` are documented in the [{doc}`molsysmt.MolecularMechanics API Reference </api/form/molsysmt_MolecularMechanics/api_molsysmt_MolecularMechanics>`].
