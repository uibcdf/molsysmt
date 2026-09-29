---
summary: Design H5MSM 0.6 persistence for MolecularMechanics
issue: uibcdf/molsysmt#256
status: open
opened: 2026-09-29
closed:
verification: inspected
area: [form, data]
guard:
normative:
blocked_by: []
supersedes: []
---

# H5MSM 0.6 MolecularMechanics persistence

**Reported:** 2026-09-29, during the H5MSM 0.5 pre-1.0 scope review.
**Status:** Open for design after MolSysMT 1.0.

## What

Design a versioned H5MSM 0.6 representation for the native
`MolecularMechanics` domain after its parameter model is sufficiently defined.
The [H5MSM 0.5 contract](h5msm_0_5_modular_layers.md) intentionally contains
no mechanics layer. This proposal must not delay MolSysMT 1.0.

## How

First define which force-field settings, atom parameters, bonded terms,
constraints, energies, and parameterization provenance belong to the native
domain. Then specify their typed file representation, physical units, index
associations, presence semantics, and compatibility rules. H5MSM 0.6 should
round-trip supported data without depending on Python object serialization.

The 0.5 writer continues to reject nonempty mechanics data before creating a
file. A default empty native mechanics object does not imply a persisted
mechanics layer. Reading a 0.5 file in a future 0.6-capable implementation
must preserve that absence rather than fabricate a parameterization.

## Why

The pre-1.0 native `MolecularMechanics` object is minimal and experimental.
Freezing its current fields into H5MSM 0.5 would make the pre-1.0 format depend
on a parameterization model that has not been settled. Deferring persistence
leaves the 0.5 topology, chemical-state, structure, and interaction contracts
free to stabilize for 1.0.

## What is measured and what is assumed

**Inspected:** The H5MSM 0.5 writer rejects nonempty mechanics data in its
native `MolSys` routes. The public rejection is guarded by
`tests/form/file_h5msm/test_public_h5msm_v05.py`.

**Assumed:** The final native mechanics model may need more than one
parameterization per molecular system. No storage benchmark or complete
parameter inventory has been performed for H5MSM 0.6.

## What was refuted

- Persisting the current minimal object in 0.5 was rejected because its
  parameter and association contracts are not mature enough to freeze.
- Silently omitting nonempty mechanics data from 0.5 was rejected because a
  successful write would claim a lossy file is a complete molecular system.

## Scope and exclusions

This proposal covers mechanics persistence in H5MSM 0.6 and compatible reads
of older files. It excludes changes to the accepted H5MSM 0.5 root layout,
the pre-1.0 `Interactions` persistence gate, and a requirement to finish the
native mechanics model before MolSysMT 1.0.

## Acceptance criteria

1. The native mechanics contract states which data are model parameters and
   which are structural observations or chemical-state facts.
2. The 0.6 schema declares units, parameterization provenance, atom and
   structure index spaces, and absent versus present-empty semantics.
3. Public read and write paths round-trip supported mechanics data and reject
   unsupported payloads without silent loss.
4. The reader handles 0.5 files without inventing mechanics data, with tests
   for mixed versions and partial domains.
5. The schema, User Guide, course, and versioned API documentation agree before
   the 0.6 format is declared public.

## Dependencies and risks

The design follows MolSysMT 1.0 and a reviewed native mechanics parameter
model. A premature codec would lock ambiguous units or particle mappings into
the file format.
