---
summary: Center misses a partially moved reference target and changes its in-place return.
issue: uibcdf/molsysmt#451
status: open
opened: 2026-10-24
closed:
severity: medium
verification: reproduced
area: [structure, coordinates]
guard:
normative:
blocked_by: []
supersedes: []
---

# Center misses a partially moved reference target and changes its in-place return

**Reported:** 2026-10-24, standalone native reproduction during addon receiving
under uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly authorized.
**Status:** open. Native contract/return correction belongs to the scientific
owner; the center addon wrapper remains absent until receiving.

## What

```python
import molsysmt as msm
puw = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     structure_indices=[0, 8, 3])
result = msm.structure.center(
    molsys, selection=[0, 2], center_of_selection=[0, 2, 4],
    structure_indices=[2, 0], center_coordinates=puw.quantity([0.1, 0.2, 0.3], 'nm'),
    in_place=True,
)
xyz = puw.get_value(msm.get(molsys, coordinates=True), to_unit='nm')
print(xyz[[2, 0]][:, [0, 2, 4]].mean(axis=1))
print(result is None, result is molsys)
```

Observed reference centers, in nm:
[[0.27640930458351415, 0.2681496712896559, 0.2992181721660826],
 [0.1778133189236676, 0.21809072030915155, 0.2591003550975411]].
The requested target is [0.1, 0.2, 0.3]. Return checks are False, True rather
than the documented successful in-place None. Unselected atoms are unchanged.

## How

center.py computes the reference center, translates only selection, recomputes
the residual and translates selection again. When the reference population is
only partly moved, that second pass does not establish the documented target.
The correction branch also assigns output=molecular_system for in-place calls.

## Why

The public contract does not declare this population combination unsupported.
A caller receives scientific coordinate edits that do not establish the target,
and a return type dependent on whether correction was attempted. The addon must
not supply a second centering formula, silently alter either selection or hide
the native return.

## What is measured and what is assumed

The values and return mismatch are reproduced without Viewer on the bundled
three-structure pentalanine. The intended semantics for a partially moving
reference need an explicit owner decision. Rejecting an unsupported population
before mutation or implementing a documented supported transformation are both
possible resolutions; no scientific definition is imposed by this report.

## What was refuted

Length quantities and explicit structure scopes are valid. Coordinates outside
the moving selection stay unchanged. No Viewer, synchronization, optional engine
or periodic reimaging participates in the reproduction.

## Scope and exclusions

The addon continues receiving native translation and the repaired PCA contracts.
It does not expose center or change native science to bypass this finding.
This report does not assert an untested alternate-syntax or GPU failure.

## Acceptance criteria

Define moving/reference population inclusion, partial overlap and disjoint
semantics. Reject unsupported combinations before writes or implement the exact
documented transform. Preserve None for successful in-place calls even on the
residual-correction branch, and independent copy ownership otherwise. Protect
weighted centers, target/unit shapes, repeated/nonconsecutive structures,
selected-scope invalidation and failed-input preservation with independent
numerical pytest references. Native return and science remain owner contracts.

## Provenance

Linux, Python 3.14.7, molsyssuite@uibcdf_3.14. Source
306e91ddaa7d47f57d1c503c8f1715ba432a8161, bundled pentalanine, standard nm.
H5MSM 0.4 warnings retained. Source evidence, not installed artifact qualification.
