---
summary: SASA engines have an implicit different periodic contract
issue: uibcdf/molsysmt#479
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, sasa]
guard:
normative:
blocked_by: []
supersedes: []
---

# SASA engines have an implicit different periodic contract

**Reported:** 2026-10-26, native audit before expert-addon receiving.
**Status:** Open; scientific resolution belongs to MolSysMT, without consumer corrections.

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

This report does not change scientific code, dependency floors, package versions
or addon semantics. No implicit preparation, unit compensation or periodic
geometry correction is authorized in the consumer.

See the [audit receipt](../../devtools/data/molsysviewer_tools_sasa_native_audit_20261026.json).
