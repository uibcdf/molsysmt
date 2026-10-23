---
summary: Heavy distances discard the second atom selection within one system.
issue: uibcdf/molsysmt#441
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: medium
verification: reproduced
area: [structure, heavy, selection]
guard: tests/structure/get_distances/test_heavy_endpoints.py
normative:
blocked_by: []
supersedes: []
---

# Heavy distances silently replace the second endpoint population

**Reported:** 2026-10-23 during scientific-owner review for the structure tools
addon, uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Filing explicitly authorized
by the principal maintainer.
**Status:** resolved in native MolSysMT. The addon continues to consume the
public scientific API.


## What

Two populations of sizes three and two should produce a (3, 3, 2) distance
array for three selected structures. Forced chunking returns (3, 3, 3) and
starts at zero, as though both populations were the first selection. The eager
first value is 0.10899963385132325 nm.

```python
import molsysmt as msm
molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    structure_indices=[0, 8, 3],
)
for mode in ['off', 'force']:
    result = msm.structure.get_distances(
        molsys, selection=[0, 2, 4], selection_2=[1, 3],
        structure_indices=[2, 0, 2], pbc=False, heavy_mode=mode,
    )
    print(mode, result.shape, msm.pyunitwizard.get_value(result, to_unit='nm')[0, 0, 0])
```

## How

In [get_distances.py](../../../molsysmt/structure/get_distances.py), heavy_eligible
admits a same-system second selection. The executor receives atom_indices only;
_DistancesReducer calculates that first population against itself. Neither the
second population nor its separate structure scope reaches this reducer.

In the alternate-unit probe, eager quantities follow the active pm standard
while heavy quantities retain nm. The output unit policy should be preserved
or explicitly documented with the endpoint repair; the population error exists
independently of that unit-label difference.

## Why

Wrong endpoint populations mean wrong scientific observables and potentially
misleading index metadata. Equal-sized disjoint populations could hide the shape
error. Automatic processing of large inputs can select the same path; auto
activation thresholds were not benchmarked in this exercise.

## What was refuted

Both routes use the same system, selected structures and pbc=False. The result
is not a unit-conversion discrepancy because dimensions and endpoint identity
already differ. Native vectors retain both populations and their physical values
under forced processing; a competing addon distance algorithm is unnecessary.

## Acceptance criteria

Implement the requested populations and structure correspondence in native
chunking, or reject unsupported combinations before scientific calculation.
Guard unequal and equal-sized disjoint populations, separate structure selectors,
repeated structure order, supported index metadata and actual numeric values.
No silently truncated, all-versus-all or relabeled replacement result is valid.

## Scope and exclusions

This is a native MolSysMT defect, reproduced without importing MolSysViewer.
The addon preserves public native options and outputs. It does not silently
rewrite heavy_mode, change standard units, substitute a different algorithm or
claim scientific validation of this affected route. Existing frozen artifacts
and publication pauses are unaffected.

## Provenance

Observed 2026-10-23 on Linux, Python 3.14.7 in molsyssuite@uibcdf_3.14. Provider
HEAD c4b71b2069b3613f0b1e340f7448f645cc80f0b4 with concurrent unrelated PDBQT
work preserved; reviewed geometry sources are unchanged. Tests use bundled
pentalanine, retaining its H5MSM 0.4 legacy-read warning. These are source
observations, not clean installed-artifact qualification.

## Implementation — 2026-10-23

The existing endpoint projection/coordinate readers were extracted from vectors
into shared private geometry delivery, with caller-specific diagnostics. Scalar
distances reuse those tools and the existing Rust Euclidean/MIC kernels, without
allocating a vector tensor. Aligned structure axes read the selected atom union
once; independent structure axes read bounded second blocks and reject unequal
lengths before numerical calculation.

The reducer preserves endpoint membership/order/repetition and computes rectangular
slabs. Its output shape and backing bytes use selected counts, not global atoms.
It preallocates resident output or retains the persistent handle; application
length presentation is applied per block before storage. Empty axes remain shaped.
Second-center calculations are no longer admitted to the flat-atom reducer; they
retain the existing center path, as do explicit pairs and two-system calculations.
One scalar slab over the work budget raises before the kernel; there is no
atom-axis tiling or whole-process memory guarantee.

The original 14 literal endpoint/unit tests failed before the fix; they exercise
unequal/equal disjoint atom sets, repeated structure order and separate structure
axes. Further guards cover native/modular delivery, actual source-coordinate
geometry, selected persistent bytes, alternate units, metadata, empty axes,
center routing, indexed PDBQT and the original bundled report. No new detector,
scientific criterion, compiled algorithm or external dependency is introduced.

## Qualification — 2026-10-23

**Contract-tested and parity-tested:** the combined scalar-distance, vector,
heavy-execution and hydrogen-bond regression passed **377 tests** in 22.05
seconds using `--receptor=llm -n 12`. The 56 warnings are 49 expected legacy
H5MSM reads and seven memory-pressure observations from intentionally tiny
configured budgets. The original bundled reproduction now returns `(3, 3, 2)`
and the expected first distance. No fail or skip occurred.

The primary guard uses literal coordinate subtraction/norms, independently of
the distance implementation, including MIC in a known orthogonal cell. It
checks actual selected indices and numeric values, spies on bounded second
reads, and asserts physical backing-file bytes and pm values for persistent
output under both forced and automatic execution. It also protects the eager
second-center route and rejects a mismatched structure scope/oversized slab
before Rust. The original 14-case guard failed before this correction.

The bundled-system doctest passed. The distance tutorial, large-ensemble
cookbook and Common Core course module 19 executed successfully. All 250
selected public docstrings passed fidelity/content validation. The final fast
gates and Sphinx outcome are recorded in the qualification receipt. This is
source-level regression evidence, not an installed release matrix, new
scientific profile validation or performance benchmark.

Receipt: [`distances_heavy_endpoints_20261023.json`](../../../devtools/data/distances_heavy_endpoints_20261023.json).
