---
summary: MIC fast path misclassifies rotated orthogonal periodic boxes
issue: uibcdf/molsysmt#257
status: resolved
opened: 2026-09-29
closed: 2026-09-29
severity: high
verification: reproduced
area: [pbc, structure, scientific-integrity]
guard: tests/rust/test_mic_pair_observations.py::test_rotated_orthogonal_box_uses_lattice_distance_in_existing_kernel
normative:
blocked_by: []
supersedes: []
---

# MIC fast path misclassifies rotated orthogonal periodic boxes

**Reported:** 2026-09-29, while preparing periodic image output for interaction
detectors under `uibcdf/molsysmt#250`.
**Status:** Resolved. The production MIC dispatcher now restricts the
Cartesian-diagonal fast path to axis-aligned boxes.

## What

The MIC dispatcher classified a rotated orthogonal box as eligible for a
Cartesian-diagonal fast path. That path subtracted the three diagonal matrix
entries independently, producing a displacement that need not differ from the
input by any integer combination of the box vectors. For the box with rows
`[[q,q,0],[-q,q,0],[0,0,1]]`, `q=2**-0.5`, and displacement
`[-1.65,-1.05,1.20]` nm, the old branch returned a length of about
0.46170445 nm. Enumeration of lattice images in a ±4 shell gives a true
minimum of about 0.47775178 nm, at image `[2,0,-1]`. A periodic distance
cannot be shorter than the minimum over actual lattice images.

The old calculation can be reproduced without the compiled extension:

```python
import itertools
import numpy as np

q = 2**-0.5
box = np.array([[q, q, 0], [-q, q, 0], [0, 0, 1.]])
raw = np.array([-1.65, -1.05, 1.20])
old = raw - np.diag(box) * np.floor(raw / np.diag(box) + 0.5)
truth = min(np.linalg.norm(raw + np.array(n) @ box)
            for n in itertools.product(range(-4, 5), repeat=3))
assert np.linalg.norm(old) < truth
```

## How

At `rust/src/mic.rs`, `prep_dist()` selected `mic_vector_ortho()` whenever
`box_is_orthogonal()` found zero row dot products. `mic_vector_ortho()` uses
only the Cartesian diagonal entries, which is valid for an axis-aligned
diagonal box, not for every orthogonal orientation. The correction restricts
that fast path to truly axis-aligned boxes; rotated orthogonal boxes use the
general reduced-cell MIC path. The new observed-pair test independently
enumerates lattice images and checks both distance and image coefficients.

## Why

The error affects periodic distances and any consumer of the shared MIC
dispatcher, including neighbor detection and interaction geometry. It can
create geometrically impossible distances and prevent a legitimate observed
image from being expressed in the original box basis. The high severity is
for scientific correctness on a valid class of periodic boxes, not for a
known frequency of rotated boxes in user data.

## What is measured and what is assumed

- **Reproduced:** The old diagonal formula gives 0.4617044549 nm for the
  example above; exhaustive search gives 0.4777517799 nm. The code block
  reproduces the inequality.
- **Inspected:** The shared production dispatcher took the diagonal branch
  for this box because its row dot products vanish.
- **Assumed:** No estimate is made of how often user trajectories contain
  rotated orthogonal boxes.

## What was refuted

- Orthogonality alone does not justify subtracting independent Cartesian
  diagonal entries. A rotated orthogonal basis supplies the counterexample.
- Recovering an image after that incorrect displacement cannot repair it:
  the displacement itself is not a lattice image of the input.

## Scope and exclusions

This report covers the shared MIC fast-path classification and the regression
on rotated orthogonal boxes. It does not redesign the triclinic reduced-cell
algorithm, the neighbor-list grid, or interaction detector result adapters;
those remain under their existing work items.

## Acceptance criteria

1. A rotated orthogonal box uses a lattice-correct MIC displacement.
2. A regression test checks its distance against independent image enumeration
   and checks that the reported integer image reconstructs that distance.
3. Existing Rust MIC and neighbor-list batteries pass; ordinary diagonal-box
   behavior remains unchanged.

## Provenance

Observed on host `nauta`, Python 3.13.14, NumPy 2.4.6, 2026-09-29, starting
from commit `d1500372a`. The reference computation above uses NumPy and the
standard library; the changed implementation uses the bundled Rust extension.

## Resolution evidence

The guard invokes the existing public-facing pair-distance Rust kernel with a
rotated orthogonal box and compares its answer with independent enumeration of
nearby lattice images. Restoring the old orthogonality-only dispatch makes
that assertion fail. The observed-pair image test also checks that the chosen
integer shift reconstructs the measured distance in the original box basis.
On 2026-09-29, the Rust battery passed 80 tests and the focused Python
interaction, MIC, neighbor, and PBC battery passed 173 tests.
