---
summary: SASA engines have an implicit different periodic contract
issue: uibcdf/molsysmt#479
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [physchem, sasa]
guard: tests/physchem/get_sasa/test_get_sasa_periodic_contract.py
normative:
blocked_by: []
supersedes: []
---

# SASA engines have an implicit different periodic contract

**Reported:** 2026-10-26, native audit before expert-addon receiving.
**Status:** Resolved on 2026-10-26; the scientific fix and its guards are native to MolSysMT.

## What
`physchem.get_sasa` silently changes periodic treatment with `engine`: native CPU automatically uses minimum images when the system has a box, while MDTraj evaluates the supplied Cartesian positions without periodic images. The public signature has no `pbc` argument and its help does not explain this distinction.

## How
```python
import numpy as np
import molsysmt as msm
puw = msm.pyunitwizard
source = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0])
carbons = msm.select(source, selection="atom_type=='C'")
two = msm.extract(source, selection=[int(i) for i in carbons[:2]])
msm.set(two, coordinates=puw.quantity([[[0.1, 0, 0], [1.9, 0, 0]]], 'nm'),
        box=puw.quantity([2*np.eye(3)], 'nm'))
for engine in ['MolSysMT', 'MDTraj']:
    area = msm.physchem.get_sasa(two, engine=engine, use_gpu=False,
                n_sphere_points=960, use_cell_list=False)
    print(engine, puw.get_value(area, to_unit='nm**2'))
```

Observed area per carbon, nm^2: MolSysMT `[0.796279855, 0.800053693]`; MDTraj `[1.207628250, 1.207628250]`. With the 2 nm box, the minimum-image separation is 0.2 nm; direct Cartesian separation is 1.8 nm. This is a geometric difference, not just quadrature noise. Inspection confirms native MIC dispatch versus unmodified `mdtraj.shrake_rupley`.

## Why
Expert addon users must know which surface is requested. Preserving native engine forwarding without an explicit periodic contract would hide a scientific choice (uibcdf/molsysmt#421; uibcdf/molsysviewer#264). No Viewer-specific periodic correction is proposed.

## Acceptance criteria
The scientific owner should decide and document explicit periodic controls and/or clearly defined engine limitations; unsupported combinations must be unambiguous. Add native pytest coverage of vacuum, box-present, opposite-face occlusion, requested nonconsecutive structures and both engines. Distinguish numerical sampling tolerances from boundary-condition semantics. Do not require a new periodic MDTraj algorithm merely to close this: a clear supported contract with guards is sufficient.

## Provenance

Measured on Linux x86-64, Python 3.14, clean source a77d41fa5fe4f460a59e9ed4ed3c67f330570031, existing ABI3 backend SHA256 f32ed73f7ef3cf3225e12fbc56b9c4236a4452d758c94661f41860ad00d82c1c; CPU only. No new package qualification.

## What is measured and what is assumed

The numerical results above are executed native-only observations, not an addon
or installed-package qualification. The frozen source and existing backend are
identified above; no new extension was built. GPU paths are unqualified.
The receipt stores the actual values and backend digest.

## What was refuted

This reproduces without Viewer or scene synchronization. The isolated-carbon
check removes the box and all other atoms, excluding periodicity and occlusion
as causes of the unit discrepancy. The two-carbon periodic case uses standard
nm throughout, excluding the separate unit-context defect as its cause.

## Scope and exclusions

The resolution changes native Python area labeling and periodic dispatch, and
forwards the same control through the bound SASA reader. It does not change
Rust algorithms, dependency floors, package versions, scene synchronization or
chemical preparation. There is no consumer-side numerical compensation.

See the [audit receipt](../../../devtools/data/molsysviewer_tools_sasa_native_audit_20261026.json).

## Resolution

A keyword-only `pbc=True` is appended after all existing arguments, retaining
the original positional API and native default. `pbc=False` requests Cartesian
SASA for either engine. `pbc=True` uses native minimum-image screening when a
box exists, and Cartesian screening without a box. MDTraj with a box now raises
`NotImplementedMethodError` for a periodic request, directing the user to the
native engine or an explicit Cartesian calculation. It no longer silently
ignores the box. The shared PBC validator checks boxes in canonical nm before
converting them to the kernel working unit.

**Contract-tested / bounded analytic evidence:** orthogonal and triclinic boxes,
nonconsecutive repeated structure lists, atom/group outputs, nm/angstrom/pm,
missing boxes, lattice translations, cell-list/brute-force agreement, invalid
periodic controls and the legacy positional call are covered. The default
MDTraj rejection guard failed on the original implementation. The scientific
registry adds an independent opposite-face carbon spherical-cap construction
but deliberately retains partial SASA evidence.

**Inspected limit:** native MIC screening excludes the sampled atom's own
periodic images. This is documented, not promoted to an all-images surface
algorithm for arbitrary small cells. Scientific validation of general periodic
cells or self-image occlusion is outside this resolution.

The new bound-reader guard checks both forwarded choices, preserved scene state
on unsupported periodic MDTraj requests, and units without geometric correction.
Existing reference-engine tests now explicitly use Cartesian screening on both
sides instead of comparing different boundary conditions.

## Verification and documentation

Local Python 3.14 CPU source checks: 271 SASA/analytic cases including the public
doctest; 144 bound SASA/table-reader cases; 491 notebook-schema cases; all 14 fast
release gates. The updated SASA tutorial executed successfully. Course and
Cookbook changes preserve every existing code cell, output and metadata.
Local HTML built with zero errors and 45 warnings; the known course heading and
MyST warning debt remains under uibcdf/molsysmt#144. This is not a full-suite,
installed-artifact, cross-platform or release qualification.

The User Guide Foundations, tool tutorial, Cookbook, all four property course
modules, bound-reader documentation and API docstring now describe the selected
contract. The docstring attributes Shrake–Rupley and links the MDTraj interface.
See the [resolution receipt](../../../devtools/data/sasa_units_periodic_20261026.json)
for commands, before/after outcomes, environment and source digests.
