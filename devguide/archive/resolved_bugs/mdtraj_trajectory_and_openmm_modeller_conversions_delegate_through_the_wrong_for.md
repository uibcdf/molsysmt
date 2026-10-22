---
summary: MDTraj trajectory and OpenMM modeller conversions delegate through the wrong forms
issue: uibcdf/molsysmt#419
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/mdtraj_Trajectory/test_to_openmm_Modeller.py
normative:
blocked_by: []
supersedes: []
---

# MDTraj trajectory and OpenMM Modeller conversions use the wrong adapters

**Reported:** 2026-10-22, when extending the conversion execution profile under uibcdf/molsysmt#181.
**Status:** Resolved; repaired routes and geometry are guarded directly and publicly.

## What

`openmm.Modeller -> mdtraj.Trajectory` rejects valid Modeller input with
`ArgumentError`. `mdtraj.Trajectory -> openmm.Modeller` reaches an OpenMM-only
extractor with MDTraj topology and raises `TypeError: 'list_iterator' object is
not callable`. Full and partial atom selections both fail.

```bash
python -m pytest tests/form/openmm_Modeller/test_to_mdtraj_Trajectory.py tests/form/mdtraj_Trajectory/test_to_openmm_Modeller.py --receptor=llm -n 12
```

Eight cases fail on the original source: direct and public calls in both
directions, with all atoms or a subset. Inputs use the existing small builder
fixtures and explicit coordinates; Modeller positions are supplied in angstroms
and trajectory structure 1 is selected in the opposite direction.

## How

The Modeller adapter imports the `mdtraj.Topology` identity adapter and passes
it a Modeller with normal digestion. The trajectory adapter imports the
`openmm.Topology` identity adapter and bypasses digestion on a foreign object;
its extractor then tries to call MDTraj's iterable chain property.

Delegate instead through each source form's existing topology converter. Keep
public validation and the existing coordinate conversion/extraction path.

## Why

Both declared container conversions are unusable even for small, nonperiodic
systems with all required information. The narrower topology routes already
work; these wrapper imports are the defect. This is execution correctness,
not an unsupported chemical interpretation or unavailable provider.

## What is measured and what is assumed

The expanded smoke suite initially reports 77 passes, two failures (including
harness controls), with both optional engines installed. The eight mirrored
regressions reproduce the failures with explicit positions and selections.
Expected coordinates are literal arrays converted to nanometers independently
of the result; no output converter supplies the oracle.

## What was refuted

Installing providers or disabling validation is not a repair. OpenMM and MDTraj
are already installed. Bypassing digestion only moves the foreign-form error
into the OpenMM extractor.

## Scope and exclusions

Correct the three source-form imports, then guard direct/public conversion, atom selection,
structure selection and coordinate units without source mutation. Periodic-box
transfer and general cross-provider fidelity are outside this bounded report.
No new API or scientific method is introduced.

## Acceptance criteria

All eight regressions pass, the expanded declared-edge profile retains both
routes, and ordinary existing form and public conversion tests continue to pass.

## Provenance

Linux x86_64, Python 3.14.7, source based on be860a74e; MDTraj 1.11.1,
OpenMM 8.6.1 installed in the shared development environment; 2026-10-22.

### Nested selection path

After correcting the two outer adapters, all-atom conversions succeed but the
trajectory-to-Modeller subset still fails. Its topology converter also imported
the MDTraj topology identity adapter instead of its own trajectory-to-topology
adapter. Two direct/public subset controls isolate that same foreign-form
mechanism in `mdtraj.Trajectory -> openmm.Topology`. Correcting the nested import
is part of this repair; validation remains enabled at public boundaries.

The repair corrects three source-form delegations and adds explicit lazy
provider requirements. Both outer directions now execute; selected topology
conversion also reaches the correct source adapter. The separate mirrored
Modeller regression module additionally guards angstrom-to-nanometer values:
`tests/form/openmm_Modeller/test_to_mdtraj_Trajectory.py`. No periodic transfer
claim is added for these container routes.

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
