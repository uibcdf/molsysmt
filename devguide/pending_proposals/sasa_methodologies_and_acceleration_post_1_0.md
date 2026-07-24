# Proposal: additional SASA methodologies and acceleration (post-1.0)

**Status:** pending (post-1.0)
**Owner:** MolSysMT
**Related:** `topomt_requested_spatial_helpers_and_sasa.md` (Part 1 — done)

## Context

`physchem.get_sasa` computes the solvent-accessible surface area with a native,
dependency-free **Shrake–Rupley** rolling-probe algorithm (Numba JIT on CPU, with
CUDA and Taichi GPU kernels and a minimum-image PBC variant), plus an optional
`mdtraj` engine. As of the Part 1 work it exposes `probe_radius` and
`n_sphere_points` (unified default 240) on both engines.

The native Shrake–Rupley path has two known limitations, neither a 1.0 blocker:

1. **Angular quantization.** Accuracy is set by `n_sphere_points`; the surface is
   sampled at discrete points, so per-atom values carry quantization noise. This
   is now user-tunable but is inherent to the numerical S–R method.
2. **O(N²) occlusion cost per frame.** For each surface point of each atom, the
   kernel scans every other atom for occlusion. The repository already ships a
   cell-list neighbour-search (`lib/structure/get_contacts_cell_list.py`) used by
   `get_contacts`, but SASA does not use it.

## Proposed work

### A. Cell-list acceleration of the native Shrake–Rupley kernel

**CPU part — DONE (pre-1.0).** A reusable CSR neighbour-search primitive
(`molsysmt/lib/structure/neighbor_list.py`: `neighbor_list_csr`, `neighbor_pairs`;
vacuum + PBC; query/ref generality) now backs a cell-list SASA kernel
(`get_sasa_cell_list` / `get_mic_sasa_cell_list`), exposed as
`get_sasa(..., use_cell_list='auto')`. It restricts the occlusion scan to
candidate neighbours (safe cutoff `2*max_radius + 2*probe`), turning the
per-frame cost from O(N²·P) to ~O(N·P) with numerically identical results
(parity tests: `tests/physchem/get_sasa/test_get_sasa_cell_list.py`,
`tests/structure/test_neighbor_list.py`).

**Remaining (post-1.0):**
- **GPU neighbour-list build.** The current CUDA/Taichi SASA kernels are still
  brute-force. The CSR layout is GPU-portable, but a GPU cell-list build needs
  atomics for cell insertion and handles warp divergence from ragged neighbour
  counts; the crossover versus the already-parallel GPU brute force is at large N.
- **Consumer migration.** `get_contacts` has been migrated onto the shared
  primitive (its cell-list path now calls `neighbor_pairs`; the old
  `get_contacts_cell_list` module was removed), covered by
  `tests/structure/test_contacts_cell_list.py`. Remaining candidates
  (`get_neighbors` threshold mode, h-bond candidate generation) are tracked in
  `neighbor_list_consumer_migration.md`.

### B. LCPO (Linear Combination of Pairwise Overlaps)

Add an analytical LCPO estimator (Weiser, Shenkin, Still, 1999), as used by Amber.

- Fast, and **differentiable** — enables SASA gradients/forces for implicit-solvent
  and scoring use cases.
- Approximate (parametrized per atom type); would ship as an alternative
  `engine`/`method`, not the default.

### C. Lee–Richards analytical SASA

Add an analytical Lee–Richards (rolling-sphere arc integration) estimator for a
more exact surface boundary than point-sampled Shrake–Rupley.

- Higher accuracy than numerical S–R at comparable or better cost.
- More complex geometry (self-intersecting arcs); larger implementation effort.

## Sequencing

A (acceleration, no new science, reuses existing infra) is the highest
value/effort item and should come first. B and C are alternative methodologies
selected via an `engine`/`method` argument; they can follow independently. None
of these change the Part 1 public surface — they add engines/flags on top of it.
