---
summary: Native SASA mislabels squared coordinate units as nm²
issue: uibcdf/molsysmt#478
status: open
opened: 2026-10-26
closed:
severity: high
verification: reproduced
area: [physchem, sasa]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native SASA mislabels squared coordinate units as nm²

**Reported:** 2026-10-26, native audit before expert-addon receiving.
**Status:** Open; scientific resolution belongs to MolSysMT, without consumer corrections.

## What
The native CPU `physchem.get_sasa` returns physically different areas when changing only the configured standard length unit. An isolated carbon should have area `4*pi*(0.17+0.14)^2 = 1.207628216 nm^2`. Results converted back to nm^2 are 1.207628216 (nm), 120.762821604 (angstrom), and 1207628.216040 (pm). MDTraj returns 1.207628250 nm^2 in all three contexts.

## How
```python
import numpy as np
import molsysmt as msm
puw = msm.pyunitwizard
source = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'], structure_indices=[0])
carbons = msm.select(source, selection="atom_type=='C'")
one = msm.extract(source, selection=[int(carbons[0])])
msm.set(one, box=None)
for engine in ['MolSysMT', 'MDTraj']:
    for unit in ['nm', 'angstrom', 'pm']:
        with puw.context(standard_units=[unit, 'ps', 'radians', 'dalton', 'e', 'dimensionless']):
            area = msm.physchem.get_sasa(one, engine=engine, use_gpu=False,
                        n_sphere_points=960, use_cell_list=False)
            print(engine, unit, puw.get_value(area, to_unit='nm**2'))
print('analytical nm^2:', 4*np.pi*(0.17+0.14)**2)
```

The native branch converts coordinates, van der Waals radii and probe radius into `length_unit`, but labels the computed values as `nm**2` unconditionally before standardization. This is independent of Viewer.

## Why
Silent scientific numerical error under a supported unit context. This blocks receiving unit-invariant SASA in the expert MolSysViewer addon (uibcdf/molsysmt#421; uibcdf/molsysviewer#264). Do not compensate in the consumer.

## Acceptance criteria
Add native pytest coverage of nm/angstrom/pm contexts with analytical isolated-carbon truth, atom/group outputs, explicit probe units, and brute-force/cell-list routes. Preserve configuration after calls. Audit common CPU/GPU output-unit wrapping; actual GPU qualification remains separate from CPU tests. Reuse existing scientific tolerance ownership.

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
