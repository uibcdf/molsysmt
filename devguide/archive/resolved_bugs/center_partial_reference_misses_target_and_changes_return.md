---
summary: Center misses a partially moved reference target and changes its in-place return.
issue: uibcdf/molsysmt#451
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, coordinates]
guard: tests/structure/center/test_center_contract.py
normative:
blocked_by: []
supersedes: []
---

# Center misses a partially moved reference target and changes its in-place return

**Reported:** 2026-10-24, standalone native reproduction during addon receiving
under uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly authorized.
**Initial status:** open. Native contract/return correction belongs to the scientific
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


## Accepted contract — 2026-10-24

The maintainer selected an explicit source/destination redesign after reviewing
both the historical implementation and tutorial. The former names are retired:
`selection` is the moving atom population; `source_center_selection` defaults to
that population and must be contained in it. `target_coordinates` and
`target_center_selection` are mutually exclusive destinations, with neither
meaning the origin. The latter uses the target's initial geometric center,
including when the target overlaps atoms that will move. Source weights address
only the source population. Weighted targets can be supplied as coordinates
obtained through the general `get_center` tool.

Partial or disjoint source/moving populations now reject before writes; no
compensation formula or repeated attempt to move an unmoved reference is used.
A different target population may be disjoint, partly overlapping or wholly
contained in the moved atoms. Each structure receives one common translation
`initial_target - initial_source`, preserving relative atomic positions.
Destination snapshots remain fixed during residual refinement.

This is a deliberate pre-1.0 keyword and default-contract change, not a
compatibility alias. A selected population now centers on itself by default.
PBC wrappers and `move_away` retain their own public arguments and delegate
using the new explicit names, selection syntax and structure scope. Tutorials,
the common course module and the standalone static-view generator migrate their
calls. No Viewer addon centering wrapper is introduced by this correction.

## Implementation and verification

The existing compiled `get_center` primitive owns centroid computation; the
existing `translate` tool owns coordinate edits. There is no additional backend
or dependency. Selection resolution uses the requested syntax; `get_center`
itself now forwards that syntax to its general selection owner. Coordinates
are compared and subtracted in explicit nm values, independent of session
presentation units and input quantity backends.

Invalid populations, conflicting destination modes, nonfinite centers/points,
unsupported destination shapes, invalid source weights and conflicting targets
for duplicate structures reject before coordinate writes. The residual branch
returns None in place and refines the existing output otherwise, avoiding a
second system copy. Native setters preserve normal selected-structure
interaction invalidation and snapshot ownership.

The independent NumPy coordinate oracle covers native MolSys and Structures,
source subsets and default moving centers, geometric and mass weights,
disjoint/overlapping target populations, repeated atoms and structures,
nonconsecutive scopes, units and rigid pair vectors. The explicit A=2/B=4/C=10
example places C at 3 nm. Alternate MDTraj selection syntax is exercised on a
writable native object and get_center is also tested on a readable MDTraj
trajectory; its unimplemented coordinate setter is not claimed as supported.

Local integration checkpoint: **262 passed in 11.56 seconds**, 12 workers,
pytest-receptor, across center/get_center, move_away, flip, PBC wrappers,
remove_overlapping_molecules and analytic structural-transform truth tests.
Twenty-seven legacy-H5MSM warnings and one existing structural-attribute-drop
warning are retained. The first draft pair-vector assertion had an incorrect
NumPy advanced-indexing shape; fixing the independent oracle did not change
production code. Broader regression and executed documentation are being
verified before publication and closure. No installed package, release or
cross-platform qualification is inferred from these source tests.

## Final local qualification — 2026-10-24

The complete structural/PBC/argument regression command uses 12 workers and
pytest-receptor:

```bash
python -m pytest tests/structure tests/pbc tests/scientific_truth/structure \
  tests/_private/argdigest tests/build/remove_overlapping_molecules \
  --receptor=llm -n 12
```

It produced **1,796 passes and one download failure in 148.87 seconds**. The
sole failure, get_neighbors test 8, could not resolve RCSB's host inside the
sandbox. Repeating exactly that node with network access passed in 8.16 seconds.
Thus all 1,797 selected cases were verified, across the original run and the
explicit network recovery; this is not represented as one entirely green run.

The final center contract module contains 195 cases. The consolidated final
contract, general-center, argument and documented workflow selection passes
**225 tests in 14.62 seconds**, with 23 retained warnings and no failures or
omissions. The shared positional-axis validator rejects negative, boolean,
nested and noninteger structure indices before writes; this also prevents
negative aliases from evading duplicate-destination checks. Empty structure
populations reject. The center docstring doctest passes (5.21 seconds). All six affected notebooks execute successfully: center, flip,
remove_overlapping_molecules, Common Core Module 16 and the Enzyme/Alzheimer
Module 46 examples. The latter preparation and rendering defects are tracked
and repaired separately in uibcdf/molsysmt#454.

Ruff lint/format, public signature validation with the explicit maintainer
redesign waiver, docstring fidelity (251 functions), and all 14 fast release
gates pass. Sphinx HTML builds successfully; the accepted pre-existing warning
population remains under uibcdf/molsysmt#144. Publication/CI evidence is separate
from these local results. No release, tag, installed artifact or full supported
platform matrix is authorized or qualified by this fix.
