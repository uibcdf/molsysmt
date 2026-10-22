---
summary: MDTraj topology to trajectory conversion ignores coordinate units selections and box
issue: uibcdf/molsysmt#420
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/mdtraj_Topology/test_to_mdtraj_Trajectory.py
normative:
blocked_by: []
supersedes: []
---

# MDTraj topology-to-trajectory conversion loses explicit geometry semantics

**Reported:** 2026-10-22, after unit-stripping warnings in the expanded uibcdf/molsysmt#181 smoke profile.
**Status:** Resolved; repaired routes and geometry are guarded directly and publicly.

## What

The declared `mdtraj.Topology -> mdtraj.Trajectory` route passes quantity values
directly to MDTraj, which strips their units. Angstrom inputs become nanometer
values without conversion, producing tenfold distances. `atom_indices` and
`box` are accepted but ignored: selected output still contains all atoms and
provided periodic cells disappear.

```bash
python -m pytest tests/form/mdtraj_Topology/test_to_mdtraj_Trajectory.py --receptor=llm -n 12
```

Original source: six failures, two passes, eight unit-stripping warnings. Both
direct and public routes reproduce each failure. Nanometer/all-atom controls
pass; the topology fixture is four atoms and coordinates contain two structures.

## How

The adapter extracts a selected topology into `tmp_item` and immediately
replaces it with `Trajectory(coordinates, item)`, using the original topology.
No explicit coordinate-unit conversion or box transfer exists.

Normalize coordinates to MDTraj's nanometers with PyUnitWizard; retain matching
source-axis positions for the extracted topology; transfer explicit row-vector
periodic cells in nanometers. Supplied coordinates describe the full source atom
axis, so selection is applied once to both topology and coordinates. Follow the
existing topology extractor's unique source-order atom selection convention.

## Why

This is silent scientific corruption for valid explicit units, not just a
conversion exception. Output shape/form alone cannot detect it. The route
already accepts coordinates, selection and box; the repair implements that
contract rather than introducing a new operation.

## What is measured and what is assumed

Literal arrays define expected Cartesian coordinates in nanometers. Tests pass
equivalent values in nanometers and angstroms and compare the actual MDTraj
`xyz` values. Separate controls compare selected atom names, coordinate slices
and independently provided triclinic cell vectors. No converter output is used
to derive expected geometry. The comparison tolerance accounts for MDTraj's
float32 coordinate storage, not for incorrect unit scaling.

## What was refuted

The unit-stripping warnings are not harmless here: angstrom tests differ by a
factor of ten. The requested subset does not merely have a different ordering:
it retains all four atoms. A supplied periodic cell is not converted differently:
it is absent entirely.

## Scope and exclusions

The topology-plus-coordinate adapter, documented geometry arguments and mirrored
regressions. No dynamics, force-field interpretation, new format or scientific
method. General extraction/reordering semantics of unrelated forms remain
unchanged. A missing coordinate array remains an invalid trajectory input.

## Acceptance criteria

Direct and public routes preserve physical values for both tested units, apply
matching source-order atom selection once, retain explicit periodic cells and
do not mutate source arrays or topology. No implicit unit stripping remains in
this route. The expanded conversion smoke profile retains the edge.

## Provenance

Linux x86_64, Python 3.14.7, NumPy 2.4.6, MDTraj 1.11.1; source based on
be860a74e, shared development environment, 2026-10-22. Local source evidence only.

The repair uses PyUnitWizard to obtain explicit nanometer values, preserves
the selected topology's source-order atom axis, and transfers provided row-vector
cells to MDTraj. A single cell broadcasts over structures; incompatible atom
and cell counts or absent coordinates fail explicitly. Eleven mirrored controls
include duplicate/reordered atom requests and source-array preservation.
The conversion tutorial and Native Forms module explain those limits while
preserving all executable notebook content and saved outputs. The public
adapter docstring includes a passing bundled-system example and explicit units.

## Verification and resolution — 2026-10-22

The expanded conversion and neighboring form/public-route suite passes **2,178
cases**, zero skips/failures, 123.67 seconds with twelve workers and Pytest
Receptor. Fifteen warnings remain: ten existing dummy-PDB-cell warnings and five
expected legacy H5MSM notices; none report unit stripping. The updated adapter's
bundled-system public doctest also passes separately. Commands, provider versions,
notebook preservation and the documentation log digest are retained in the
[receipt](../../../devtools/data/conversion_execution_engines_20261022.json).

The full Sphinx HTML build exits 0 with 711 warnings and zero errors, unchanged
from the previous whole-site warning baseline. This is not a warning-clean
site; broader documentation debt stays in uibcdf/molsysmt#144. The fourteen
fast release gates and applicable Ruff check/format controls pass. No new release
matrix, package build, tag or publication is implied.

The actual adapter docstring also renders through Sphinx autodoc/Napoleon with
no page diagnostics. Its guard is
`devtools/tests/test_public_api_docs.py::test_mdtraj_topology_geometry_docstring_renders_without_rst_errors`.
One case passes; two Sphinx 11 deprecation warnings remain Python-level notices,
not page-rendering errors. This guard checks reStructuredText, not scientific
geometry, which is protected by the separate mirrored conversion tests.
