---
summary: Minimum distances reuse first-population weights for the second center.
issue: uibcdf/molsysmt#444
status: open
opened: 2026-10-24
closed:
severity: medium
verification: reproduced
area: [structure, weights]
guard:
normative:
blocked_by: []
supersedes: []
---

# Minimum distances reuse first-population weights for the second center.

**Reported:** 2026-10-24 during addon receiving under uibcdf/molsysmt#421 /
uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Status:** open. The MolSysMT scientific team owns the correction; Viewer keeps
this new wrapper pending rather than altering native parameters or formulas.


## What

Independent second-population weights are accepted but ignored in the minimum
center distance. Native values for the reproduction are
[0.6595507508555509, 0.5834060321652554, 0.6595507508555509] nm. Independent
weighted centroids give [0.7720171238073741, 0.674794639416701,
0.7720171238073741] nm.

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     structure_indices=[0, 8, 3])
indices, distances = msm.structure.get_minimum_distances(
    molsys, selection=[0, 2], selection_2=[10, 25],
    structure_indices=[2, 0, 2], center_of_atoms=True,
    center_of_atoms_2=True, weights=[1., 1.], weights_2=[1., 3.], pbc=False,
)
```

## How

[get_minimum_distances.py](../../molsysmt/structure/get_minimum_distances.py)
passes weights_2=weights to get_distances. This replaces the caller's second
weights rather than forwarding them. Independent NumPy average calculations on
both coordinate populations expose the wrong second centroid.

## Why

Different populations can intentionally use different weights, including masses
or numeric weighting. Silently changing one endpoint changes the scientific
observable. Different population sizes may expose a validation error instead of
a wrong value; both outcomes need coverage.

## What was refuted

The reproduction uses the same source and explicit structures in both calculations,
with PBC disabled and values converted to nm. It imports no Viewer. The maximum
helper forwards its second weights independently in the reviewed source.

## Acceptance criteria

Correct the native forwarding and guard actual scientific values, source indices,
independent endpoint weights/domains and unchanged caller inputs. The maintainer
explicitly requests a pytest contract matrix covering get_distances, get_neighbors,
get_minimum_distances and get_maximum_distances: native forms/H5MSM, population
sizes/order, two sources, repeated/nonconsecutive structures, PBC/units, eager/
heavy paths, supported output metadata, empties/errors and selection/weight
combinations. Use independent references, not only parity with a shared defective
implementation. The detailed request is in the owning issue comments and applies
to both uibcdf/molsysmt#444 and uibcdf/molsysmt#445.

## Scope and exclusions

No addon algorithm, scientific fix or hidden route/parameter substitution is
introduced here. Closed #441 repaired chunked scalar endpoint populations;
this report records a separate wrapper-level scientific delegation defect.
Existing artifact coordinates and publication pauses remain unchanged.

## Provenance

Observed on Linux, Python 3.14.7 in molsyssuite@uibcdf_3.14, source
bc21428312b6945c9c8926611721713c5ca3fbd2. Bundled pentalanine's H5MSM 0.4
warning is retained. This is source evidence, not installed-artifact qualification.
