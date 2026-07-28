# Triclinic cell-list completeness (Rust neighbour list and cell-list SASA)

**Status:** **RESOLVED (2026-07-25)** — implemented in `neighbors.rs` and `sasa.rs`.
The Rust cell list and cell-list SASA are now correct on triclinic boxes, validated against
an all-pairs ±2 ground truth (neighbour list) and the brute-force SASA (0 difference) on
mild and heavily-skewed boxes. Kept for the record of the diagnosis and fix.
Archived 2026-07-28.
**Relates to:** [`rust_kernel_redesign_beyond_faithful_ports.md`](rust_kernel_redesign_beyond_faithful_ports.md),
[`wrap_to_mic_triclinic_not_minimum_image.md`](../resolved_bugs/wrap_to_mic_triclinic_not_minimum_image.md).
**Crate:** `rust/src/neighbors.rs`, `rust/src/sasa.rs`.

## Context

The minimum-image (MIC) wrap was unified onto a **reduced-cell** mechanism
(`mic::mic_vector`) for every *wrap-based* kernel — distances, angles, dihedrals, the
set/shift dihedral ops. That fixes the correctness bug of the ±1 (27-image) search, whose
shell can miss a second-neighbour minimum image on skewed cells (see
`wrap_to_mic_triclinic_not_minimum_image.md`).

The **grid-based** kernels — `neighbor_list_csr_multi` (behind `get_contacts`/
`get_neighbors`) and the cell-list SASA — were left on their existing centred wrap, because
their triclinic incorrectness is **not only** in the wrap. It is also in the grid gathering.

## The evidence

Neighbour list on a mildly-skewed triclinic box (`[[6,0,0],[1.5,6.5,0],[0.8,1.1,7]]`, 250
atoms, cutoff 1.2 nm), against a ±2 ground-truth over all ordered pairs:

| implementation | pairs found | vs ground truth (1802) |
|---|---|---|
| ground truth (±2, all pairs) | 1802 | — |
| **Rust (reduced wrap)** | 1782 | **20 missing, 0 spurious** |
| Numba (centred wrap) | 1806 | 78 missing, 82 spurious |

Rust with the reduced wrap is far better (no false positives, and a true distance for every
candidate it gathers), but it still misses 20 true neighbours. Those 20 are pairs whose true
minimum-image distance is within the cutoff but which the **grid's ±1 fractional stencil
never gathers**: on a skewed box, a ±1 neighbourhood in the (oblique) fractional basis does
not cover a Cartesian sphere of radius `cutoff`, so some near atoms fall in fractional-far
cells. This is independent of the wrap — fixing the wrap removed the spurious pairs but not
the missing ones.

## The task

Make the grid gathering complete on triclinic boxes. The standard approaches:

1. **Build the grid on the reduced cell** (short, near-orthogonal basis vectors), sizing
   cells by the reduced vector *lengths* (not the diagonal) so a ±1 fractional stencil
   covers `cutoff`. This is the cleanest fix and reuses the reduction already computed for
   the wrap; the care is in cell sizing when reduction reorients the vectors.
2. **Widen the stencil for triclinic** so it covers `cutoff` in Cartesian — a per-axis
   radius `ceil(cutoff / cell_width_along_axis)` accounting for skew. Simpler but slower
   (larger stencil) and needs the skew-aware width.

Either must be validated against the ±2 all-pairs ground truth on random skewed boxes (the
harness above), not against the Numba oracle, which is itself wrong here.

## Why it was deferred, not rushed

`neighbor_list_csr_multi` is the hot path behind `get_contacts`/`get_neighbors` (the common
path after the cell-list threshold change). A half-correct grid change to it is worse than
the status quo, and a correct triclinic cell list is a real algorithmic piece deserving its
own change and validation. Until then the grid kernels keep their committed behaviour
(bit-for-bit with Numba), and the wrap-based kernels carry the correctness fix.

**Scope note:** for MD-normal boxes (tilt within the OpenMM/LAMMPS reduction limit and
`cutoff < L/2`), the grid is already complete; this bites only skewed boxes read from
non-reduced input. Reducing the input box on load (as OpenMM/LAMMPS do) would also avoid it.


## Resolution

Three fixes made the grid kernels correct on triclinic (and small) boxes:

1. **Perpendicular-thickness grid sizing** (`grid_dims`): cells sized by `V/|b_j×b_k|`, not
   the box-vector lengths, so a ±1 stencil covers the cutoff on a skewed box.
2. **Correct lattice fractional binning**: `cell()` uses `inv^T · p` (the true fractional
   coordinate), not `inv · p`, which only agrees for orthogonal boxes and mis-binned
   triclinic ones so the ±1 stencil no longer matched spatial ±1. This was the dominant
   error (the perpendicular sizing alone left the misses).
3. **Reduced-cell minimum image** for the candidate distance (`mic::mic_vector`), so a
   gathered candidate gets its true minimum-image distance rather than the single centred
   wrap.

Plus a `n<3` fix (`axis_cells`): on a box smaller than 3× the cutoff the ±1 periodic
stencil revisited cells and double-counted; the stencil now visits each cell once.

Cost: the triclinic neighbour list is ~1.7× the orthogonal one (the 8-corner reduced wrap
per candidate); orthogonal is unchanged. Correctness first; the wrap could be shortened
later with an early-exit around the centred round.
