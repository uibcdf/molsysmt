---
summary: Neighbors ignore the explicit second molecular system in distance fallback.
issue: uibcdf/molsysmt#445
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: medium
verification: reproduced
area: [structure, selection]
guard: tests/structure/test_distance_family_contract.py
normative: docs/content/user/tools/structure/distance_family.md
blocked_by: []
supersedes: []
---

# Neighbors ignore the explicit second molecular system in distance fallback.

**Reported:** 2026-10-24 during addon receiving under uibcdf/molsysmt#421 /
uibcdf/molsysviewer#264. Filing explicitly authorized by the maintainer.
**Initial status:** open. The MolSysMT scientific team owns the correction; Viewer keeps
this new wrapper pending rather than altering native parameters or formulas.


## What

The nearest distance to a deliberately translated reference is returned as about
0.53477614 nm, although the actual minimum to the requested target is
9.734511628068665 nm.

```python
import molsysmt as msm
puw = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     structure_indices=[0, 8, 3])
reference = msm.copy(molsys)
msm.set(reference, coordinates=msm.get(reference, element='atom', coordinates=True)
        + puw.quantity([10., 0., 0.], 'nm'))
neighbors, distances = msm.structure.get_neighbors(
    molsys, selection=[0], selection_2=[10, 25],
    molecular_system_2=reference, structure_indices=[0],
    structure_indices_2=[0], n_neighbors=1, pbc=False,
)
```

## How

[get_neighbors.py](../../../molsysmt/structure/get_neighbors.py) uses the explicit
second system to disable the cell-list route but omits it from the fallback
get_distances call. Second atom indices are consequently interpreted in the
primary source. Review same_set inference for independent sources as well;
second-source identity should not be inferred from missing selection parameters.

## Why

Cross-system neighborhoods silently address the wrong coordinate domain. Equal
atom populations/index ranges can hide this error. Native tests need sources
with deliberately distinct coordinates and independent selectors.

## What was refuted

Both sources are valid copies with the same atom axis; only the reference is
translated. Explicit pbc=False rules out wrapping into the original unit cell.
The reference stays unchanged. NumPy coordinates of the requested target expose
the wrong distance without importing Viewer.

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


## Resolution — 2026-10-24

Neighbors now forward the explicit second molecular system and infer self identity
only for an implicit same-source population. Physical self exclusion retains
distinct coincident atoms; repeated selections do not make an atom its own
neighbor. Stable local-index ties, zero counts, bounds, directed pair sorting,
filters, supported CSR/metadata and internal disk-handle retirement are guarded.
The Rust cell-list sort follows the same tie policy. Unsupported combinations
raise explicitly.

The [shared family qualification and contract-to-test inventory](minimum_distances_reuses_first_population_weights.md#resolution-and-qualification--2026-10-24)
is the single source for executed commands/scopes, 686 Python tests, public
doctests, Rust checks, documentation execution and coverage limits. These
guards run in the source smoke and matching local tier. Consumer migration and
installed/release qualification remain separate.
