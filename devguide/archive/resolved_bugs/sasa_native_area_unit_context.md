---
summary: Native SASA mislabels squared coordinate units as nm²
issue: uibcdf/molsysmt#478
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: high
verification: reproduced
area: [physchem, sasa]
guard: tests/physchem/get_sasa/test_get_sasa_units.py
normative:
blocked_by: []
supersedes: []
---

# Native SASA mislabels squared coordinate units as nm²

**Reported:** 2026-10-26, native audit before expert-addon receiving.
**Status:** Resolved on 2026-10-26; the scientific fix and its guards are native to MolSysMT.

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

The resolution changes native Python area labeling and periodic dispatch, and
forwards the same control through the bound SASA reader. It does not change
Rust algorithms, dependency floors, package versions, scene synchronization or
chemical preparation. There is no consumer-side numerical compensation.

See the [audit receipt](../../../devtools/data/molsysviewer_tools_sasa_native_audit_20261026.json).

## Resolution

The native result is now labeled with `length_unit**2` before PyUnitWizard
standardization. Coordinates, atomic radii, probe radius and periodic boxes are
aligned in that working length unit. MDTraj retains its documented nm² engine
boundary. No kernel rebuild or physical-radius change was needed.

**Contract-tested / analytically checked:** the new unit guard varies input
coordinates and standard units independently across nm, angstrom and pm, uses
three explicit probe units, native brute-force/cell-list and MDTraj providers,
atom/group outputs, repeated nonconsecutive structures, and a partially occluded
selected atom. It also covers native, composite and MDTraj input forms and
checks source/configuration preservation. Before the fix, the corrected first
170-case guard failed 76 cases and passed 94; the earlier fixture-authoring run
is not scientific failure evidence.

The common native output boundary also covers the retired GPU-selector
fallback. No GPU backend is supported or qualified; tests exercise CPU fallback,
not CUDA or Taichi kernels.

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
