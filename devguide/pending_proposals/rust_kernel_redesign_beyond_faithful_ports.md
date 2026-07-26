# Rust kernels: what a redesign buys beyond the faithful ports

**Status:** evidence-based proposal (2026-07-24), partially resolved 2026-07-26 — A, B and E
done; D closed as a negative result; C and F open. See the status table in §5.
**Relates to:** `rusterization_pilot_conclusions_and_adoption.md`,
`linear_algebra_backend_for_rust_kernels.md`,
`rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`,
`rust_numba_coexistence_and_cut_plan.md`.
**Code location:** `experiments/rust_kernels/` on `main` (the pilot branch was merged and
deleted).

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

### D. Columnar (SoA) layout for SIMD — **measured, and it is a negative result**

The hypothesis was: coordinates are `[n_structures, n_atoms, 3]`; every distance kernel
loads three contiguous doubles and does scalar arithmetic; with separate `x[]`, `y[]`,
`z[]` a kernel could process 4-8 atoms per SIMD lane. This was ranked here as the largest
*structural* lever, and it is scoped more broadly in
`rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`.

**It was benchmarked (2026-07-26) and SoA is slower than AoS**, in both instruction-set
regimes. Microbenchmark: all-pairs squared distances with a cutoff condition, n = 4000
atoms, identical arithmetic, only the layout differs.

| build | AoS `[n,3]` | SoA `x[],y[],z[]` | SoA speedup |
|---|---|---|---|
| baseline (SSE2) | 18.5 ms | 19.6 ms | 0.94x |
| `-C target-cpu=native` (AVX2 + FMA) | 13.5 ms | 19.4 ms | 0.69x |

The reason is the *access pattern*, not the arithmetic. A pair kernel touches atom `j` once
and then walks `k`: with AoS, atom `k`'s three doubles arrive on **one** cache line; with
SoA they come from **three** separate streams, tripling the number of live cache lines and
the pressure on the hardware prefetcher. The lanes SoA would fill are never the bottleneck
— the loads are. Note also that AVX2 *widened the gap*: the better layout got faster and
SoA did not, so vectorisation does not rescue it.

**Recommendation: drop D for the pair-distance kernels.** Do not undertake the data-model
refactor on SIMD grounds. If `rusterization_hybrid_columnar_ecs_arrow_graph_engine.md` is
ever pursued, it must be justified by Arrow interop / zero-copy / attribute-centric
storage arguments, *not* by an expected SIMD win in the compute kernels, and it must
re-measure before touching the geometry hot paths. This is recorded so nobody pays for the
refactor twice.

(One caveat on the benchmark itself: an earlier branch-free variant of this comparison
reported AoS at 0.0 ms because LLVM proved the accumulator unused and deleted the loop.
That run was discarded. Only the cutoff-condition version above, whose result is observed,
is reported here.)

### E. Reduced cell for the triclinic MIC — **done**

Instead of searching 27 images per vector, reduce the cell once per structure and the
direct fractional wrap is already the minimum image. Removes a 27x factor **and** fixes a
correctness limitation: the ±1 shell is *not* exhaustive for strongly skewed cells (see
`pending_bugs/wrap_to_mic_triclinic_not_minimum_image.md`). The rare case where the better
algorithm is also the more correct one.

Implemented across the whole Rust MIC surface (greedy lattice reduction + factored 8-corner
wrap), with the ±1/±2 all-pairs search retained as a test-only oracle. See
`triclinic_cell_list_completeness.md` (RESOLVED).

### F. SIMD instruction set: fixed AVX2 baseline vs runtime multiversioning

This is a *packaging* lever, not a kernel one, and it was raised as "a fixed AVX2 baseline
or runtime multiversioning for a portable wheel — it should help a bit and cannot hurt".
Measurement says the second half of that is **not true**: it can hurt.

The crate today builds with `opt-level = 3, lto = true` and **no** `target-cpu`, i.e. the
x86-64 baseline (SSE2). Rebuilding the same sources with `-C target-cpu=native` on a host
with `avx avx2 fma`:

| kernel | orthogonal | triclinic |
|---|---|---|
| `neighbor_list` 1 x 4000 | 2.0 → 1.8 ms | 4.4 → 3.7 ms |
| `neighbor_list` 50 x 3000 | 70.8 → 65.1 ms | 132.6 → 103.5 ms |
| `sasa_cell_list` | 16.2 → 16.2 ms | 40.8 → 30.7 ms |
| `mic_distances` (dense) | 554 → **693 ms** | 1125 → **1307 ms** |

So AVX2 buys 1.1-1.3x on the cell-list kernels, nothing on orthogonal SASA, and **loses
16-25% on the dense distance kernels** — the single most expensive path in the profile
(§3). Enabling it globally would be a net regression on the workload that matters most.
Plausible causes for the regression (unverified): wider vectors reducing the effective
number of in-flight loads, and AVX/SSE transition or downclocking effects; the point for
the decision is that the sign is not uniform, so "cannot hurt" is false.

The four distribution options:

1. **Baseline (current).** One portable wheel, runs everywhere, leaves some headroom on the
   table. No user compilation.
2. **Fixed `x86-64-v3` (AVX2) baseline.** Simple, but bakes in the `mic_distances`
   regression *and* drops every pre-2013 x86 CPU and non-v3 cloud instances — an
   `ILLEGAL_INSTRUCTION` crash at import, not a slow path. For a scientific library shipped
   to unknown hardware this is the worst option.
3. **Runtime multiversioning.** Compile selected functions once per feature level and
   dispatch on `is_x86_feature_detected!` (directly with `#[target_feature]`, or via the
   `multiversion` crate). This is what numpy and the BLAS libraries do. The wheel stays a
   single portable artifact, users compile nothing, and no CPU is excluded.
4. **Compile from source** (`pip install --no-binary`, conda-forge with a `target-cpu`
   flag). Always available as an escape hatch for someone tuning a cluster; never the
   default path we ask users to take.

**Recommendation: option 3, but per-kernel and measurement-gated — not globally.** The
mechanism is right and it is the only option that keeps one portable wheel while adapting
at runtime. But the measurements above say the *policy* must be "opt a kernel in only when
its own benchmark shows a win", because a blanket AVX2 build regresses the hottest kernel.
Concretely, `neighbor_list` and the triclinic `sasa_cell_list` are candidates;
`mic_distances` is explicitly not.

Costs to weigh against a 1.1-1.3x on two kernels: the dispatch attribute must be applied
and maintained per function; multiversioned functions are compiled N times (build time,
binary size); and every opted-in kernel needs its numerical output checked on *each*
feature level, since a different vectorisation can reassociate a reduction and change the
last bits. Given that Rust's value in this migration was cold start and allocation removal
rather than arithmetic throughput (see `rusterization_pilot_conclusions_and_adoption.md`),
this is a **low-priority, post-cut** item. It pairs naturally with stage 3 of
`rust_numba_coexistence_and_cut_plan.md` (CI multiplatform wheels), where the build matrix
is being touched anyway — do it there or not at all.

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

### Status, 2026-07-26

| lever | status |
|---|---|
| A. PCA covariance as a matrix product | done (see `linear_algebra_backend_for_rust_kernels.md`) |
| B. Route contacts through the cell list | done for `get_contacts` (threshold lowered to 400 atoms; crossover measured near 500) |
| C. Fused multi-observable passes | open, but measured negligible — the candidate pass is ~2.5 ms |
| D. SoA layout for SIMD | **closed as a negative result** — SoA is 0.94x / 0.69x vs AoS |
| E. Reduced cell for the triclinic MIC | done, and it fixed a correctness defect |
| F. SIMD multiversioning | open, low priority, post-cut; do it with the CI wheel matrix or not at all |

Once C and F are settled, this proposal has no live items and should be archived: the
remaining redesign work lives in `rust_numba_coexistence_and_cut_plan.md` (packaging) and
`rusterization_hybrid_columnar_ecs_arrow_graph_engine.md` (data model, now without its
SIMD justification).

## 6. The framing that matters

"Can the kernels be more optimal if we escape the transported code?" — yes, but the
evidence says the win is **almost never inside a kernel**. It is in choosing a different
algorithm at the dispatch level (B, E), a different API shape (C), or recognising what an
operation actually is (A). The faithful ports were the correct first move precisely because
they make these the *next*, separable decisions instead of entangling them with the
migration.

The two levers that promised a win from *how the code is compiled or laid out* rather than
from what it computes — SoA (D) and wide SIMD (F) — are the two that measurement cut down
to nothing or to a per-kernel trickle, one of them with a regression on the hottest path.
That is the same lesson as §2, one level lower: every time the redesign question was
answered by measurement instead of intuition, the answer was "the algorithm, not the
machine".
