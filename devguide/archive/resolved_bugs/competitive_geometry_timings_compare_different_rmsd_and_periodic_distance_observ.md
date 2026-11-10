---
summary: Competitive geometry timings compare different RMSD and periodic-distance observables.
issue: uibcdf/molsysmt#673
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [performance, tests]
guard: devtools/tests/test_benchmark_geometry_semantics.py
normative:
blocked_by: []
supersedes: []
---

# Competitive geometry compares different observables

## What

The competitive RMSD suite compares MolSysMT/MDAnalysis unaligned coordinate
RMSD with MDTraj's default optimal-superposition RMSD. Its distance suite also
compares MolSysMT's default periodic distances with nonperiodic kernel/third-party
distances. The route labelled MDTraj distance actually calls SciPy cdist.
These are invalid comparative workloads, not scientific defects in those tools.

## How

On ca76d93b4, a four-atom/three-structure PDB retains a rigid 2 nm translation
and a separate local deformation. The original MDTraj case returns approximately
0.000345 nm for the translation instead of 2 nm. For points 0.9 nm apart in a
1 nm periodic cell, public MolSysMT returns 0.1 nm while nonperiodic routes
return 0.9 nm. Both new independent coordinate guards fail. Raw JUnit/events,
source hashes and the bounded execution are retained privately as
benchmark-567-semantics-directed (2 failures, no resource stop).

## Why

A ratio between different observables cannot support an efficiency conclusion.
Preserve original timings/baseline bytes. Use explicit unaligned RMSD, explicit
nonperiodic distances and actual MDTraj pair evaluation. Verify all routes on
actual prepared coordinates before timing; capture differing precision and
payload overhead rather than promising identical APIs. #567 owns the separate
versioned comparability/measurement contract and advisory disposition.

## Acceptance

Retain the original rigid-translation, local-deformation, periodic-boundary and
full pair-grid assertions. Incorrect scientific results must stop the benchmark
before timing. No native molecular function, detector criterion, algorithm or
citation claim changes. No historical competitor ratio is reclassified as valid.


## Resolution — 2026-11-09

Explicit unaligned RMSD and nonperiodic full-pair distances now evaluate the
same observable before timing, and the MDTraj distance route actually invokes
MDTraj. Independent translation/deformation/PBC cases and deliberate incorrect
third-party results retain mandatory assertions. Both nm and angstrom policies
are covered. All 172 benchmark controls pass on clean 3547b0977; all fourteen
fast gates pass on combined ecf05b066. No native scientific algorithm is changed
and no historical ratio becomes valid retroactively.

Receiving record: [benchmark_comparability_receiving_567_673_676_20261109.json](../../../devtools/data/benchmark_comparability_receiving_567_673_676_20261109.json).
