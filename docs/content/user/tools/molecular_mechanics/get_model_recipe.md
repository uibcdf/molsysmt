(Tutorial_Get_model_recipe)=
# Get model recipe

*Inspecting the physical model that a mechanics adapter actually constructs.*

A stored setting is a request, not proof that an engine used it. Before an
energy or force calculation, inspect the model with
{func}`molsysmt.molecular_mechanics.get_model_recipe`:

```python
import molsysmt as msm

model = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
recipe = msm.molecular_mechanics.get_model_recipe(model)
recipe['requested']['constraints']
recipe['effective']['n_constraints']
recipe['effective']['nonbonded']
```

The result is a detached `molsysmt.model_recipe@1` dictionary. For native or
other supported chemistry, this query constructs an OpenMM System and reads
its settings. It creates no Context or integrator, chooses no device and
neither prepares chemistry nor changes coordinates. Parameterization can
consume provider memory; this is not a metadata-only lookup.

## Requested and effective settings

`requested` distinguishes stored values, explicit conversion arguments and
MolSysMT defaults. A stored `None` leaves a setting unset; a conversion keyword
`None` is an explicit override. The query has no model-override keywords:
edit an independent native model first if you want a different model.

A declared implicit model deactivates a conflicting *global default* water
model. That entry has `origin='inapplicable_default'`, `value=None` and an
`inactive_default` recording the omitted default. Two nonempty solvent families
explicitly requested in storage or conversion arguments are rejected. Neither
the source nor application defaults are edited. Resource-name lookup retains
its separate documented precedence; it does not construct or validate a model.

`effective` reads the actual particle and constraint counts, periodicity,
default box vectors and NonbondedForce settings. Box vectors are rows. Length
quantities follow your active PyUnitWizard policy. Configured dispersion,
reaction-field and Ewald settings are retained even when the chosen nonbonded
method makes them inactive. A custom force inventory retains provider names;
it does not claim to characterize every possible custom energy expression.

| Current construction control | Disposition |
| --- | --- |
| forcefield, water_model, implicit_solvent | Adapter resource selection, with explicit family-conflict checks |
| constraints | Physical policy translated to the engine; effective constraint count is inspected |
| non_bonded_method, switch_distance, dispersion_correction, ewald_error_tolerance | Forwarded through supported construction routes; configured engine values are inspected |
| cutoff_distance, flexible_constraints, rigid_water, hydrogen_mass | Nonempty independent requests are rejected |
| salt_concentration, kappa, solute_dielectric, solvent_dielectric | Nonempty independent requests are rejected; standard OBC recipes remain available |
| partial_charge, atom_ff_type | Stored per-atom overrides are rejected because this constructor does not apply them |
| legacy MolecularMechanics.formal_charge | Rejected as a mechanics override; ChemicalStates formal charges remain chemical assignments |

The same admission protects public construction of System/Context/Simulation,
energy, forces and minimization. It never silently discards an unsupported
request. A refusal identifies the actual fields with catalog diagnostic
`MSM-ERR-MECH-001`. Supplying an already parameterized engine model is a separate
route: that model is authoritative, including its own custom parameters.

## Structure and provenance

For native chemistry, `structure_indices=None` chooses the first stored
structure, or permits coordinate-free chemistry. An explicit selection must
contain exactly one valid structure associated with the reference chemical
state. It supplies the construction box/state context, not a trajectory
observable. A modular H5MSM input reads that context without loading the whole
coordinate trajectory or named analyses. The result retains the source
structure index after internal projection.

For a supplied System, Context or Simulation, leave `structure_indices=None`.
The report inspects that model without changing its live Context. Construction
controls, force-field names and resources remain unknown rather than being
inferred from particle counts. A compact report cannot recreate arbitrary
custom forces; retain the original parameterized model for exact reproduction.

`software`, `resources` and detached `attribution` identify the adapter and
versions used now. OBC construction credits the actual variant and
[Onufriev, Bashford and Case (2004)](https://doi.org/10.1002/prot.20033), separately
from executed OpenMM software. Optional Ackredit failure preserves the completed
report and emits a diagnostic. Inspecting a previously constructed model does
not invent its historical scientific provenance.

The mechanics domain and this query remain experimental. This is neither an
engine-neutral numerical-equivalence claim nor a complete reproducibility
archive. Hardware, temperature, integrators and other execution settings remain
separate. The read-only addon mirror is available as
`view.addons.molsysmt.molecular_mechanics.get_model_recipe()`; it reads the current
system without choosing the visible structure or changing the scene.

See {ref}`user-foundations-support-molecular-mechanics` and
{ref}`Tutorial_Get_forces` for scientific and execution limits.
