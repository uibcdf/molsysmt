(user-foundations-native-world-classes-molsysmt-molecularmechanics)=
# MolecularMechanics

The native `MolecularMechanics` domain, accessed through `molsys.molecular_mechanics`,
holds prepared force-field parameters and non-bonded interaction settings.
It remains experimental. Default H5MSM 1.0 output preserves its admitted
parameters and original assignment reports; explicit 0.5 output refuses stored
mechanics. Persistence does not certify parameterization or execute a model.
See {ref}`user-tools-form-h5msm-10` for the versioned storage contract.

---

## Overview and Role

As a user, `molsysmt.native.MolecularMechanics` is the object holding physical mechanics parameters required for energy evaluations, molecular dynamics simulations, or electrostatics calculations.

---

## Internal Attributes

Per-atom parameters share the row axis of the `atoms_ff` table. Scalar settings
are separate attributes:

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| **`forcefield`** | String or `None` | Declared solute parameterization request; a label does not prove completed assignment. |
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
Construction rejects two nonempty explicitly requested solvent families. An
implicit model suppresses a conflicting global water default, without changing
the source. Clear a stored implicit model explicitly before requesting water.
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


## Legacy Translation

`molsys.molecular_mechanics.get_openmm_System_parameters()` returns an
engine-specific keyword dictionary; it does not execute a model. The native
class can also be imported from `molsysmt.native`. Constraint translation is
shared with the public OpenMM conversion: `None`/`none`, `hbonds`, `all bonds`
and `h angles` accept underscores, spaces and hyphens. In particular,
`all_bonds` selects **all bonds**, rather than only bonds involving hydrogen.
Unknown policies are rejected. The method supports the standard keyword-only
`skip_digestion` validation control and diagnoses an unavailable optional engine.

This legacy dictionary is not a generic constructor recipe. Individual OpenMM
constructors accept different keyword sets, and returning a value does not prove
that a physical model consumed it. Prefer the public conversion and evaluation
tools with their documented capability/refusal contracts. The broader requested-
versus-effective contract is available through
{func}`molsysmt.molecular_mechanics.get_model_recipe`. This separate query reads
compiled settings without a Context, records origins and refuses unsupported
requests. It does not add independent dielectric/screening tuning. Supplied
parameterized models retain unknown construction provenance.
