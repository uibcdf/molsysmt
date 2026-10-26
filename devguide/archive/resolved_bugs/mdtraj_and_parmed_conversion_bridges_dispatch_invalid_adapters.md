---
summary: MDTraj and ParmEd conversion bridges dispatch invalid adapters.
issue: uibcdf/molsysmt#463
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/parmed_Structure/test_bridge_contract.py
normative:
blocked_by: []
supersedes: []
---

# MDTraj and ParmEd conversion bridges dispatch invalid adapters

**Reported:** 2026-10-26, during the ParmEd execution-profile expansion under
uibcdf/molsysmt#181.
**Status:** resolved. Source-specific delegation restores all three routes.

## What

The initial route execution produces three failures and twelve passes:

```bash
python -m pytest tests/conversion_truth/test_declared_native_edges.py tests/conversion_truth/test_declared_pdb_edges.py -k parmed --receptor=llm -n 12
```

`mdtraj.Topology -> parmed.Structure` raises a callable error inside the OpenMM
identity extractor. `mdtraj.Trajectory -> parmed.Structure` imports a nonexistent
plural-named converter. `parmed.Structure -> openmm.Modeller` supplies the wrong
selection keyword to the coordinate getter.

## How

Both MDTraj adapters select a converter owned by the wrong input form. The
trajectory adapter additionally imports `to_parmed_Structures` rather than the
registered singular name. The ParmEd-to-Modeller bridge has the same foreign
identity-adapter mistake and calls `get_coordinates_from_atom(atom_indices=...)`
instead of `indices=...`.

The repair uses existing source-specific topology converters and structural
getters. Coordinate and periodic geometry conversion uses PyUnitWizard and
existing PBC tools. The selected topology and coordinate axes must agree;
OpenMM Modeller represents the first selected structure and its cell. Conversion
orchestration remains in the adapters; no new geometry algorithm is needed.

## Why

Discoverable conversions fail at runtime for ordinary in-memory molecular systems.
A static graph audit cannot detect invalid implementation imports or a converter
invoked on the wrong source object. This is a MolSysMT dispatch defect rather than
an unavailable optional provider.

## What is measured and what is assumed

The initial fifteen-route run took 14.17 seconds with twelve workers and Pytest
Receptor. It stopped at each failing direct call, so that run alone does not prove
that the public call has the same failure. A separate mirrored direct/public guard
covers both calls, atom selection, structure selection and independent literal
geometry. The twelve initial mirrored cases all failed in 6.02 seconds before the repair.

## What was refuted

Provider installation is not the cause: twelve newly selected routes execute in
the same interpreter, and the traces identify invalid MolSysMT imports/arguments.
No new parser, scientific detection method or compiled numerical routine is needed.

## Scope and exclusions

Restore the three broken bridges and their supported topology/geometry contracts.
This does not certify arbitrary force-field parameter transfer or every ParmEd
conversion field. Missing source chemical or mechanical assignments are not inferred.
The broader conversion execution issue remains partial, and release qualification
is separate from this local source regression.

## Acceptance criteria

- All fifteen newly profiled routes execute directly and through public conversion.
- The mirrored guard verifies selected topology/geometry alignment and source retention.
- Topology-only MDTraj input remains topology-only; trajectory input retains all selected structures.
- Modeller coordinates and cell come from the first selected structure.
- Normal argument validation, lazy dependencies and unit policy remain active.

## Provenance

Local Linux development environment, Python 3.14; exact package versions and tested
source hashes will accompany the bounded execution receipt for uibcdf/molsysmt#181.


## Resolution and validation — 2026-10-26

The source adapters retain normal argument digestion and lazy provider guards.
Atom selections use source order when the topology exporter does, and structure
selections also reorder the cells. The adapters reuse structural getters, general
PBC conversion and the existing OpenMM box setter. Shared cells are broadcast as
a view before selecting output cells, without a trajectory-sized repeated table.

The final regression passes 2,514 tests with no failures or skips in 142.33 seconds
using `--receptor=llm -n 12`; the mirrored bridge module contains 76 cases. Four
converter doctests pass, and the updated Cookbook and Common Core module execute
successfully. The [bounded receipt](../../../devtools/data/conversion_execution_parmed_20261026.json)
records exact commands, dependency versions, source hashes and the separate
execution/fidelity/release scope. See the [operational guide](../../conversion_execution.md)
for current profile commands and remaining debt.

Ruff lint/format and the fourteen fast gates pass. The full-site HTML command
exits zero with pre-existing notebook-schema diagnostics recorded under
uibcdf/molsysmt#144; the changed examples execute, but no clean-site claim is made.
