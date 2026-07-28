# Conversion Fidelity Matrix and MolSysDict Schema Evolution

**Status:** partially implemented; current untracked fidelity WIP has confirmed contract gaps

**Priority:** P0 to restore an executable fidelity gate and close the staged
WIP gaps; P1 for the Tier 1 matrix; P2 for the schema migration

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

## Current WIP Gap Audit — 2026-07-26

The implemented first slice remains valid for the tracked tests, but it is not
a release claim for the stronger untracked fidelity work now present in the
working tree.

Three untracked test modules currently expose 38 failures:

| Test module | Current result |
| --- | ---: |
| `test_conversion_report_native_scopes.py` | 13 failed |
| `test_coordinate_trajectory_fidelity.py` | 4 failed |
| `test_pdb_fidelity.py` | 21 failed, 1 passed |

The failure set is not one missing function. It contains at least six
independent gaps:

1. missing audit-scope helper APIs, which prevent the untracked release audit
   from importing;
2. no `scope` field on `ConversionIssue`;
3. no exhaustive schema-driven audit for the native dictionary forms;
4. strict mode that does not reject losses outside the chemical subset;
5. independent `evidence`, `temperature`, `skip_digestion`, and PDB parsing
   defects;
6. a separate PDB-fidelity workstream with multiple identifier, loss-reporting,
   and strictness causes.

The canonical evidence, boundaries, acceptance criteria, and ordered resolution
are recorded in
[`conversion_fidelity_wip_contract_gaps.md`](../pending_bugs/conversion_fidelity_wip_contract_gaps.md).
That bug record supersedes any interpretation that the current untracked audit
surface is already green.

### Required Closure Order

1. Establish the audit-scope contract and a backward-compatible
   `ConversionIssue.scope`.
2. Audit native dictionary forms exhaustively against the declared attribute
   schemas, and apply strictness to every audited scope.
3. Repair the independent schema and adapter gaps in separate focused changes.
4. Resolve PDB fidelity after the scope contract is stable.

These stages are intentionally separate. They must not be collapsed into one
large commit because a passing result would then provide weak evidence about
which contract was actually repaired.

The second stage is itself incremental. Its first three earned exhaustive
profiles are:

1. `molsysmt.Structures -> molsysmt.StructuresDict`;
2. `molsysmt.Topology -> molsysmt.TopologyDict`;
3. `molsysmt.MolSys -> molsysmt.MolSysDict`, composed from the first two and a
   separate molecular-mechanics/state-association audit.

An audit profile must classify the complete declared semantic contract of its
source form. It must not infer serialization fidelity solely from the target
form's `attributes` mapping: that mapping describes query capability, not
necessarily what a particular converter writes. Derived attributes count as
preserved when their source information remains representable.

Schema or adapter expansion remains stage 3. For example, the stage-2
`StructuresDict` audit must first report an existing temperature or bioassembly
payload as a loss; adding fields that preserve that payload is a separate,
focused repair.

Stage 3 does not include every test that requests a new exhaustive route.
Ordinary-conversion preflight bypass, central atom-inventory classification,
thermodynamic dictionary fields, and the `skip_digestion` signature are focused
repairs. Native projection, builder, XYZ, DCD, and XTC exhaustive profiles are
route-promotion decisions and may be scheduled or explicitly deferred
independently. PDB `evidence` and header/identifier parsing remain in the
dedicated PDB stage.

### Critical-Path Boundary

The conversion matrix must not become a monolithic requirement to implement
hundreds of low-priority routes before unrelated library-wide consolidation can
advance.

- Shared audit, strictness, alignment, and silent-loss defects are pre-1.0
  blockers.
- Advertised Tier 1 directions require executable, honest contracts, but may
  declare unavoidable target-model loss.
- Existing non-exhaustive routes may remain as accepted baseline debt when they
  are visible and do not regress.
- Tier 2/3 and low-priority route expansion is deferred unless it reveals a
  shared correctness problem.

Progress is measured by classified contractual coverage and zero new
unclassified debt, not by forcing every registered edge to become lossless.

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

- The staged WIP gaps in
  [`conversion_fidelity_wip_contract_gaps.md`](../pending_bugs/conversion_fidelity_wip_contract_gaps.md)
  are resolved, and the conversion audit imports and executes.
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
