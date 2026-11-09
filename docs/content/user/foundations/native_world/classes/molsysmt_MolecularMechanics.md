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
| **`implicit_solvent`** | String or `None` | Requested physical solvent variant, for example `'OBC1'` or `'OBC2'`, independently of the solute field. |
| **`water_model`** | String or `None` | Explicit-water model request, separate from implicit solvation. |
| **`constraints`** | String or `None` | Stored policy such as `'hbonds'` or `'none'`; container `None` leaves it unset. |
| **`partial_charge`** | Numerical column | Partial atomic charges for each atom `(n_atoms,)` in elementary charge `e`. |
| **`atom_ff_type`** | Label column | Prepared force-field or parameter typing labels on the same atom axis. |
| **`partial_charge_assignment`**, **`atom_type_assignment`** | Optional reports | Original named-model provenance, cleared when the corresponding property is replaced. |
| **`non_bonded_method`** | String | Non-bonded interaction method (e.g. `'PME'`, `'NoCutoff'`). |

Physical model names and settings belong here; engine classes, force-field XML
files and device objects do not. Engine selection belongs to the executing
operation or requested external form. Adapters translate supported choices and
refuse incompatible ones. Current conversion reads supported stored mechanics
settings before fallback defaults. An explicit keyword wins, including
`implicit_solvent=None` to override a stored model without editing this domain.
An implicit model takes precedence over a water-model argument; clear it
explicitly before requesting only explicit water.
For constraints, store `'none'` to retain an explicit no-constraints request;
an unset container field uses the operation's default. An explicit conversion
keyword `constraints=None` requests no constraints for that call.

Use `msm.get(molsys, constraints=True)` to inspect that stored policy. The
Boolean is a reader flag: False omits the attribute; a missing stored setting
returns None. The same flags apply to other scalar mechanics settings, including
unit-bearing parameters and settings whose stored values are themselves Boolean.
Reads do not construct a physical model, fill operation defaults or certify
engine support. These queries work on MolSys, MolecularMechanics and
MolecularMechanicsDict; native `molsys.get(...)` shares the contract on MolSys.

OBC1 and OBC2 denote distinct mathematical variants. OpenMM currently executes
its standard OBC recipes; a stored label or tuning parameter does not certify
engine support or completed parameterization. Its dielectric/screening tuning
fields are not yet independently forwarded by the converter. Consult
{ref}`supported mechanics <user-foundations-support-molecular-mechanics>` for
the effective recipe and its limits. The optional Ackredit capture records
the actual constructed variant and executed engine/version; reading saved
OpenMM XML performs no new calculation and does not reconstruct that separate
bibliography.

Within one application-owned Ackredit session, implicit-model construction and
OpenMM solvation with native ion replacement share a software reference for
the OpenMM version actually used. Each operation retains its own contextual
use; solvation does not inherit the implicit-model paper. The native-ion
preparation history keeps its detached solvation reference even without
Ackredit. These records do not qualify a complete simulation protocol.
---

## Invariants and Performance

Stored `partial_charge` queries return detached float64 arrays in elementary
charge. For a partly populated column, `pandas.NA`, `None` and `NaN` become
`numpy.nan`; an absent or entirely missing column returns `None`. Explicit
indices retain their order and repetitions, including an empty array for an
empty selection of a partly populated column. Reading does not replace missing
charges, edit the stored nullable dtype, or certify assignment completeness.


`mechanics.copy()`, Python copies and enclosing `MolSys` copies preserve stored parameters, producer
reports and supported extension state through the same copy memo, without
running a constructor or legacy restoration. Mutable mechanics data remain
independent. This does not add mechanics persistence to H5MSM 0.5.

- Native charge values use elementary charge independently of the session's unit
  policy. {func}`molsysmt.build.assign_partial_charges` does not require a charge
  presentation standard and preserves the caller's policy. The quantity-returning
  {func}`molsysmt.physchem.get_partial_charges` requires that standard.
  Atom masses in `Da` are obtained through public atom attributes; they
  are not stored in this container.
- Merging concatenates prepared columns in input and selected atom order.
  Columns missing from a contributing input are cleared with a warning. Empty
  selections contribute nothing. Scalar settings come from the first input.
- Combining inputs or selecting atoms invalidates named assignment reports with
  a warning: the original reports do not describe the combined atom graph.
  A single full input retains detached reports. Input data are not modified.

---

## API Documentation

Use {func}`molsysmt.basic.convert` for conversion and the
{doc}`form tools reference </api/form/api_form>` for form discovery and capabilities.
