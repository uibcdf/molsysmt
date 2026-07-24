# Rust kernels: what a redesign buys beyond the faithful ports

**Status:** evidence-based proposal (2026-07-24), pending decision.
**Relates to:** `rusterization_pilot_conclusions_and_adoption.md`,
`linear_algebra_backend_for_rust_kernels.md`,
`rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`.
**Pilot location:** branch `experiment/rust-numba-pilot`, dir `experiments/rust_kernels/`.

## 1. The question

The migration ported 96 of the 97 CPU kernels *faithfully* — same algorithm, same
floating-point structure, parity against Numba as the gate. That was the right discipline
for a safe migration, but it deliberately gave up any gain that requires thinking of a
better routine. This proposal asks: **where is that gain real, and how should it be
pursued so effort lands where the time actually is?**

## 2. First correction: the obvious in-kernel micro-optimisations are already done

Three suspected quick wins were checked and were already present in the *original* Numba:

- the self-distance matrix already iterates `kk in range(jj+1, n)` and mirrors, so it does
  the N(N-1)/2 work, not N²;
- the SASA occlusion loop already `break`s as soon as a sphere point is occluded;
- `get_distances` already exploits symmetry.

Speculating kernel by kernel had a hit rate of 1 in 3 here. **The margin is not inside the
kernels.** It is one level up, in decisions a faithful translation could not touch.

## 3. Where the time actually goes (measured, not guessed)

End-to-end profile of real MolSysMT calls (TcTIM, 3983 atoms, 1 structure; pentalanine
trajectory, 62 atoms, 5000 structures), warm (JIT already compiled):

| operation | warm wall clock |
|---|---|
| `get_contacts` (trajectory, 5000 structures) | 2732 ms |
| `get_sasa` (protein) | 628 ms |
| `get_contacts` (protein Cα, threshold) | 493 ms |
| `get_rmsd` / `get_least_rmsd` / `get_radius_of_gyration` (traj) | ~255 ms each |
| `get_center` (protein) | 236 ms |
| `get_neighbors` (protein Cα, threshold) | 18 ms |

Two facts dominate the picture and neither is an in-kernel cleverness problem:

1. **`get_contacts` on a trajectory computes the full dense distance matrix.** 2.3 s of
   its 2.9 s is the distance kernel; it materialises an N×N matrix per structure and then
   thresholds, when a contact query only needs the pairs under the threshold. The
   cell-list primitive built for block-2 already answers exactly this and is not on this
   path.
2. **`gc.collect` is a first-class cost.** In the mixed profile it was **1.8 s of 5.0 s**;
   in `get_contacts` alone, 0.48 s. That is the Python garbage collector tracing the
   per-operation temporaries the naturally-written Numba allocates — the same allocation
   pressure the Rust ports already remove by doing arithmetic on the stack (verified:
   50 `get_rmsd` calls, 47 KB input, 4.2 KB Python-side peak; `PyReadonlyArray` borrows
   numpy's buffer, and `wrap_to_pbc` mutates in place at the same address).

## 4. The redesign opportunities, ranked by evidence

### A. PCA covariance — proven, and needs no Rust

Already documented in `linear_algebra_backend_for_rust_kernels.md`: the covariance build
is a mis-transcribed matrix product, and `X.T @ X` is 48-132x faster. The archetype of
"trapped in the translation" — we nearly ported the triple loop faithfully. **Do this
regardless of the migration's fate**; it is a numpy fix.

### B. Route contact/neighbour queries through the cell list

`get_contacts` on a trajectory is the single largest real cost measured. It should not go
through the dense distance matrix at all — the cell-list primitive already exists. This is
an algorithmic complexity change (O(N²) → ~O(N)) at the dispatch level, not a kernel
rewrite, and it is where the largest wall-clock win on real data lives.

### C. Fused multi-observable passes over a trajectory

`get_center`, `get_radius_of_gyration` and `get_rmsf` each sweep the whole trajectory
independently, and each came out a **tie** in the block-10 benchmark precisely because
they are memory-bound: the arithmetic is trivial, the cost is reading the coordinates. The
only lever is to stop re-reading — a "compute these observables in one pass" API. No
in-kernel change helps.

### D. Columnar (SoA) layout for SIMD

Coordinates are `[n_structures, n_atoms, 3]`. Every distance kernel loads three contiguous
doubles and does scalar arithmetic. With separate `x[]`, `y[]`, `z[]` a kernel processes
4-8 atoms per SIMD lane. This is the largest *structural* lever, but it changes the data
model, not the kernel, and is already scoped in
`rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`.

### E. Reduced (Niggli) cell for the triclinic MIC

Instead of searching 27 images per vector, reduce the cell once per structure and the
direct fractional wrap is already the minimum image. Removes a 27x factor **and** fixes
the correctness limitation noted in `wrap_to_mic_triclinic_not_minimum_image.md` (the ±1
shell is not exhaustive for strongly skewed cells). The rare case where the better
algorithm is also the more correct one.

## 5. How to pursue it — and when

1. **Profile real workloads first, always.** Speculation lost 1-in-3 here; the profile
   found that `get_contacts`-via-dense-matrix and GC pressure dominate, which no amount of
   staring at kernels would have surfaced. Many of the 96 kernels never appear in a real
   profile and should not be touched.
2. **Do A and B now, independently of the migration.** A is a numpy fix; B is a dispatch
   change over an existing primitive. Neither needs Rust to be the default, and both beat
   any per-kernel micro-optimisation.
3. **Defer C, D, E until after the cut decision.** While Numba is the oracle, every
   algorithmic change must be justified against it and the parity gate becomes noise. Once
   Rust is *the* implementation, redesign is ordinary work behind property tests. Doing it
   before the cut pays the parity tax twice.

## 6. The framing that matters

"Can the kernels be more optimal if we escape the transported code?" — yes, but the
evidence says the win is **almost never inside a kernel**. It is in choosing a different
algorithm at the dispatch level (B, E), a different data layout (D), a different API shape
(C), or recognising what an operation actually is (A). The faithful ports were the correct
first move precisely because they make these the *next*, separable decisions instead of
entangling them with the migration.
