# Conversion Fidelity Matrix and MolSysDict Schema Evolution

**Status:** partially implemented; remaining work pending

**Priority:** P1 for the Tier 1 matrix, P2 for the schema migration

The fidelity classifications for chemical bonds and any future interaction or
chemical-state payload must follow the semantic boundaries proposed in
[Attribute-Centric Molecular-System Architecture](attribute_centric_molecular_system_model.md).
That proposal does not change the implemented MolSysDict 0.1 contract.

## Why

MolSysMT's conversion graph is a central product feature, but form parity alone
does not establish conversion fidelity. A conversion can return a valid object
while silently dropping IDs, hierarchy, bonds, units, periodic boxes, trajectory
metadata, or the requested atom and structure subsets.

The July 2026 audit found and fixed four concrete contract violations:

- native atom extraction could sort topology while leaving structural arrays in
  request order, mislabelling coordinates;
- `MolSys -> MolSysDict` ignored atom and structure subsets;
- `MolSys -> mdtraj.Trajectory` could combine a full topology with selected
  coordinates;
- H5MSM could materialize missing bond metadata as the literal string `<NA>`.

The audit also established that `MolSysDict` schema 0.1 is narrower than native
`MolSys`: it has no component records and carries only structure IDs, time, box,
and coordinates. Expanding it without a new schema version would create an
unreviewed compatibility change.

## Implemented first slice

`tests/conversion_truth/` now provides a deterministic system with string IDs,
multiple hierarchy levels, typed and untyped bonds, an irregular time axis,
multiple structures, and triclinic boxes. The first slice verifies:

- aligned atom and structure selection for native extraction, MolSysDict, YAML,
  and MDTraj;
- declared-state round trips through MolSysDict;
- exact native-core round trips through H5MSM;
- explicit single- and double-precision H5MSM tolerances;
- preservation of missing H5MSM bond metadata;
- usable public bond metadata arguments in `MolSysBuilder.add_bond`.

## Remaining Tier 1 fidelity matrix

### How

1. Generate the matrix from the explicit form registry and direct conversion
   graph; do not maintain an unrelated hand-written form list.
2. For every route, classify each semantic field as:
   - exact;
   - tolerance-bound;
   - intentionally unavailable in the target model;
   - unsupported and rejected explicitly.
3. Exercise atom subsets, non-monotonic structure subsets, empty optional data,
   missing values, string IDs, bonds, hierarchy, and triclinic boxes.
4. Replace broad `except: pass` blocks in Tier 1 parity tests with dependency-aware
   skips and failures that identify the form and route.
5. Add representative round trips for MDTraj, OpenMM, PDB, PSF, DCD, and XTC.
   Tests must assert only target-representable semantics and separately assert
   every intentional loss.
6. Add a no-regression report to CI. A new Tier 1 edge must have a fidelity
   classification before it can be considered contractual.

### Acceptance criteria

- Every Tier 1 direct edge has an executable fidelity classification.
- No Tier 1 test suppresses an unexpected conversion exception.
- Topology and atom-dependent arrays are always aligned after selection.
- Units and numerical tolerances have an explicit reason.
- Intrinsic target-model losses are visible in developer documentation.

## MolSysDict next schema

### Decision required

Choose between keeping `MolSysDict` intentionally compact or introducing a new
schema version that can preserve the complete native structural payload. Do not
extend version 0.1 in place.

### Proposed schema work

1. Define version 0.2 or 1.0 fields for components, velocities, B factors,
   occupancy, alternate locations, bioassemblies, temperature, potential energy,
   and kinetic energy.
2. Specify canonical units, shapes, null handling, and whether every field is
   optional.
3. Reject unsupported future versions explicitly and provide a 0.1-to-new-version
   migration function.
4. Preserve 0.1 reading indefinitely through the 1.x compatibility window.
5. Add schema fixtures, malformed-input tests, full/partial round trips, and
   documentation examples before advertising full `MolSys` fidelity.

### Acceptance criteria

- Old 0.1 fixtures remain readable and retain their current interpretation.
- New payloads round-trip every field declared by the new schema.
- Unknown versions fail with an actionable diagnostic.
- The User Guide and all four MolSysBuilder course modules describe the selected
  schema boundary and have executable examples.

## Explicit non-goals

- Treating all third-party formats as lossless.
- Changing H5MSM's default float precision without storage and performance data.
- Adding a new dependency or a new trajectory backend as part of fidelity work.
- Combining the schema migration with Arrow, Polars, DuckDB, or Rust exploration.
