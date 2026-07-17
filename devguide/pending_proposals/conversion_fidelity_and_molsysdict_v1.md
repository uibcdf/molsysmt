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

### Pre-1.0 promotion scope

The pre-1.0 conversion contract must not leave strategically central adapters
classified as experimental merely because their target models are narrower than
native MolSysMT. Tier 1 means that a documented scope is stable and executable;
it does not mean that the form represents every molecular-system attribute.

The following cohorts are explicit pre-1.0 Tier 1 promotion targets. Promotion
is performed per form only after its declared read, write, selection, unit,
missing-data, and intentional-loss scope has executable evidence.

1. Trajectory and simulation exchange: `file:gro`, `file:dcd`,
   `mdtraj.DCDTrajectoryFile`, `mdtraj.XTCTrajectoryFile`, `file:h5`, and
   `mdtraj.HDF5TrajectoryFile`.
2. MDAnalysis interoperability: `MDAnalysis.Universe`,
   `MDAnalysis.AtomGroup`, and `MDAnalysis.Topology`.
3. Chemical and drug-design exchange: `rdkit.Mol`, `openff.Molecule`,
   `openff.Topology`, `string:smiles`, `file:smi`, and `file:mol2`.
4. Topology and mechanics exchange: `file:psf` and `parmed.Structure`.

A promotion gate requires:

- no declared conversion route in the contractual scope is broken;
- declared attributes are publicly deliverable;
- optional dependencies are guarded explicitly rather than hidden by broad
  exception handling;
- selections and structure subsets remain aligned whenever the form can
  represent them;
- units, precision, missing values, and target inference have explicit tests;
- unavoidable losses are represented by the conversion report and strict mode;
- documentation states directional or reduced support instead of implying a
  round trip that the target model cannot provide.

Adapters that cannot meet this gate before 1.0 must be deliberately narrowed or
removed from the advertised scope. They must not remain accidentally
experimental without a decision.

**Implementation checkpoint (2026-07-17):** the first three promotion cohorts are
complete for `file:gro`, `molsysmt.GROFileHandler`, `file:dcd`,
`mdtraj.DCDTrajectoryFile`, `mdtraj.XTCTrajectoryFile`, `file:h5`, and
`mdtraj.HDF5TrajectoryFile`, plus `MDAnalysis.Universe`,
`MDAnalysis.AtomGroup`, and `MDAnalysis.Topology`. Their reduced read scope,
cursor or active-frame preservation, unit boundaries, non-monotonic subsets,
subset alignment, velocities, thermodynamic metadata, triclinic boxes, and
chemical-state import have executable tests where applicable. AtomGroup
conversion no longer reintroduces its parent atoms, and MDAnalysis self
conversion now materializes atom and frame subsets. The adapter validator now
rejects every unreachable Tier 1 attribute declaration even when the same debt
existed in the historical baseline.

The chemical/drug-design cohort is complete for `rdkit.Mol`,
`openff.Molecule`, `openff.Topology`, `string:smiles`, `file:smi`, and
`file:mol2`; `parmed.Structure` and `file:psf` are also promoted from the topology/mechanics
cohort. Tests cover rich atom/bond chemistry, E/Z and R/S stereo, conformer and
atom subsets, complete partial charges, local duplicate IDs, reduced SMILES/SMI
semantics, Tripos types and `ar`/`am` bonds, multiple ParmEd frames and boxes,
and explicit unsupported-input rejection. PSF tests additionally cover source
IDs, CHARMM atom types, partial charges, complete explicit connectivity without
invented bond orders, atom/mechanics subset alignment, and self-copy output.
All promoted forms have zero unreachable declarations. The global adapter audit
has 101 accepted unreachable declarations across 10 non-Tier-1 forms, down by
320 from the baseline. Write/append extensions outside the documented read
contracts remain pending.

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
