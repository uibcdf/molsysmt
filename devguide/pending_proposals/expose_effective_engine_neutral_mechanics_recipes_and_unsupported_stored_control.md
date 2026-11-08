---
summary: Expose effective engine-neutral mechanics recipes and unsupported stored controls.
issue: uibcdf/molsysmt#582
status: open
opened: 2026-11-05
closed:
verification: inspected
area: [api, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Effective mechanics recipes and engine capabilities

## What

Define an engine-neutral way to identify an effective mechanics recipe and
which stored controls a selected execution adapter consumes. Physical model
choices must remain distinct from backend names, resources, implementation
versions and execution devices. Do not design the public API as an OpenMM
keyword mirror.

## How

During #580, the experimental MolecularMechanics domain was found to store
solute_dielectric, solvent_dielectric, kappa, salt_concentration and
cutoff_distance, but current OpenMM construction signatures do not consume
those independent controls. Corrected OBC1/OBC2 construction uses the engine's
standard model recipes: mbondi2 radii, ACE term, dielectric constants 1/78.5,
zero screening and the engine default cutoff when a cutoff method is selected.
Current documentation explicitly limits that contract; storing arbitrary
fields is not proof they are applied. No modified-field energy experiment has
been performed for this proposal.

Consider a named physical configuration and adapter-owned capability mapping,
with an explicit effective recipe or a refusal for unsupported requested
controls. Preserve compatible units and distinguish field absence, defaults
and explicit requests. Expose only supported useful tools; no placeholder API
or generic graph of speculative engines is requested.

## Why

General mechanics settings are intended for several engines, even though
OpenMM is the first execution provider. A reusable contract should let other
engines translate physics and report limits rather than duplicating OpenMM
classes/resources in the native domain. This also supports reproducibility and
Ackredit attribution of the actual executed recipe.

## Acceptance and scope

- Review public physical names, parameter units, default/override semantics and
  requested-versus-effective settings before adding new arguments.
- An unsupported tuning request must have a clear disposition; no silent claim
  that an arbitrary stored setting was applied.
- Validate any new adapter controls with actual parameter/energy/force responses,
  units and source preservation, not metadata shape alone.
- Keep model-family naming, native ownership, engine dependencies and attribution
  separate. No H5MSM mechanics persistence or backend-independent numerical
  equivalence is implied.
- #580's explicit OBC variants and #581's constraint translation remain bounded
  repairs. This follow-up requires its own prioritization and design; no automatic
  release deferral or new initial-1.0 gate is established here.

## Provenance

Source base d2c0882ede355e475a3b8f8a6e618d5021d01ba1 and #580 working changes,
2026-11-05. Inspected native field declarations and OpenMM adapter signatures.
Related: #421 / PR #543 and uibcdf/molsysviewer#264.

## Bounded legacy-route observation — 2026-11-08

A parameter-dictionary probe on source `731bf01ea8a07e3ad8a7477700c4ae1e24730062`
confirms that
`MolecularMechanics(non_bonded_method='no_cutoff', constraints='all_bonds').get_openmm_System_parameters()`
returns `openmm.app.HBonds`, rather than the requested `openmm.app.AllBonds`.
No Context, force field, simulation or energy calculation was constructed.
This observed legacy-helper translation mismatch does not demonstrate the same
defect in supported public conversion, which has its own constraint-list oracle
under #581.

Include this direct legacy helper in the requested/effective-control review.
The current `get_forces` construction route already refuses unsupported stored
overrides; that bounded protection does not certify every legacy method. The
wider engine-neutral recipe contract and its source/energy validation remain
pending.
