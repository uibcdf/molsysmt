# Rust kernels: what a redesign buys beyond the faithful ports

**Status:** RESOLVED — all seven levers decided; archived 2026-07-26.
**Relates to:** `rust_numba_coexistence_and_cut_plan.md`,
`linear_algebra_backend_for_rust_kernels.md`,
`pending_proposals/rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`,
`rust_kernel_optimization_guide.md`.
**Code location:** `experiments/rust_kernels/` on `main`.

> **RESOLVED — every lever decided, four implemented and three closed as negative or
> not-worth-doing.** The proposal below is retained for design provenance and for the
> measurements behind each decision; it does not define current behaviour, and it is not a
> work queue. The durable rules were migrated to the normative
> `devguide/rust_kernel_optimization_guide.md` before archival, as were the remaining
> per-kernel candidates (its section 9) — nothing live is left only in this file.
>
> **Implemented:** A (PCA covariance as a matrix product), B (`get_contacts` routed through
> the cell list, threshold at 400 atoms), E (reduced-cell minimum image — which also fixed a
> correctness defect on skewed boxes, see `archive/resolved_bugs/` and
> `triclinic_cell_list_completeness.md`), and G (what the compiler emitted:
> libm `floor` calls in the innermost loops, a latency-bound reduction in the 8-corner wrap,
> loop-invariant branches, `ArrayView` indexing, recomputed invariants). G landed in commit
> `4530fac65` and is worth 1.46x/1.39x on the dense distance matrices and up to 1.70x on the
> SASA family.
>
> **Closed without implementing, each on a measurement:** C (fused multi-observable passes —
> the candidate pass is ~2.5 ms), D (columnar/SoA layout — measured 0.94x baseline and 0.69x
> under AVX2 against the current AoS, i.e. *slower*), F (fixed AVX2 baseline or runtime
> multiversioning — baseline, `x86-64-v2` and `x86-64-v3` are equal within noise once G
> landed, so the single portable wheel stays).
>
> **Regression evidence:** 80 `cargo test` unit tests; 264 Python tests in `tests/rust/`
> (including `test_mic_neighbors_battery.py` against an independent ±2/±3 oracle, and
> `test_hot_path_lint.py`, which guards the G defect class *and* verifies that its own lint
> fails on a planted regression); 601 further tests through the public API
> (`tests/rust tests/pbc tests/physchem tests/structure tests/lib`). Green as of 2026-07-26.

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
kernels**, at the level of *which arithmetic they do*. It is one level up, in decisions a
faithful translation could not touch.

> **Amended 2026-07-26.** That conclusion holds for the arithmetic, but it was drawn from
> reading *source*. Reading the emitted *assembly* found a large in-kernel margin that no
> amount of source-level staring would have shown: three libm calls in the innermost loop
> of the hottest kernel, and a serial dependency chain in the triclinic wrap. Together they
> were worth 1.4-1.5x on the dense distance matrices. See §4.G — and take it as a method
> correction: for a kernel that is already the right algorithm, the next question is not
> "what else could it compute" but "what did the compiler actually emit".

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
`../resolved_bugs/wrap_to_mic_triclinic_not_minimum_image.md`). The rare case where the better
algorithm is also the more correct one.

Implemented across the whole Rust MIC surface (greedy lattice reduction + factored 8-corner
wrap), with the ±1/±2 all-pairs search retained as a test-only oracle. See
`triclinic_cell_list_completeness.md` (RESOLVED).

### F. SIMD instruction set: fixed AVX2 baseline vs runtime multiversioning

**Resolved: neither. Keep the portable baseline wheel.**

This is a *packaging* lever, not a kernel one, and it was raised as "a fixed AVX2 baseline or
runtime multiversioning for a portable wheel — it should help a bit and cannot hurt". The
first measurement seemed to say the second half was false (AVX2 *hurt* dense distances by
16-25%). The second measurement, after §4.G, says the **first** half is false too: there is
nothing there to win.

The crate builds with `opt-level = 3, lto = true` and no `target-cpu`, i.e. the x86-64
baseline (SSE2). Same sources at three microarchitecture levels, after §4.G:

| kernel (n = 4000) | baseline | `x86-64-v2` | `x86-64-v3` (AVX2+FMA) |
|---|---|---|---|
| `mic_distances` orthogonal | 200.9 ms | 199.6 ms | 198.1 ms |
| `mic_distances` triclinic | 409.3 ms | 437.5 ms | 401.4 ms |
| `distances` orthogonal | 281.3 ms | 287.2 ms | 288.9 ms |
| `neighbor_list` 50 x 2000 ortho/tric | 17.9 / 19.1 ms | 16.5 / 17.5 ms | 17.7 / 19.0 ms |
| `sasa_cell_list` ortho/tric | 21.2 / 35.6 ms | 19.9 / 33.5 ms | 19.7 / 35.3 ms |

All within noise. **The apparent AVX2 effects measured earlier — both the 1.1-1.3x gains and
the dense-distance regression — were artifacts of how `f64::floor` was being lowered**, not
of vector width. Once the libm calls are gone (§4.G), these kernels are bound by dependency
chains and memory traffic, and the instruction set stops mattering.

So:

- **Baseline (current, keep it).** One portable wheel, runs everywhere, and it is now
  measured *not* to be leaving performance behind.
- **Fixed `x86-64-v3`.** Gains nothing here and turns every pre-AVX2 CPU into an
  `ILLEGAL_INSTRUCTION` crash at import. Never ship this.
- **Runtime multiversioning** (per-function clones dispatched on `is_x86_feature_detected!`,
  the numpy/BLAS approach) is the *right mechanism* if a win ever exists — portable wheel, no
  user compilation, no CPU excluded — but there is currently nothing for it to win. Revisit
  only when a specific kernel's own benchmark shows a gap, and then multiversion that kernel,
  not the crate. Note the interaction: inside an SSE4.1+ clone `f64::floor` is one
  instruction, so `fast_floor` would be redundant there — which is exactly why the portable
  build is already at parity and multiversioning has nothing to add.
- **Building from source** with `-C target-cpu=native` stays available to anyone tuning a
  cluster; it is not a path users should need.

### G. What the compiler emitted — the one real in-kernel win

This lever was not in the original list because it is invisible in the source. It came from
disassembling the built `.so`, and it is the largest single-kernel gain of the whole exercise.

**On the x86-64 baseline there is no floor/round instruction** (`roundsd` is SSE4.1), so
`f64::floor()` lowers to an indirect libm call. The minimum-image wrap does three per
displacement vector — three calls in the innermost loop of the O(N²) distance kernels — and a
call in the loop body also makes the loop unvectorisable, so the whole body stayed scalar.
Note this is a JIT/AOT asymmetry rather than a language one: Numba compiles for the *host*
CPU via llvmlite, so its `np.floor` was always a single instruction.

Three changes followed, all bit-identical and all validated against the existing 262-test
MIC/neighbour battery and the ±2 independent oracle:

| change | effect |
|---|---|
| `mathlib::fast_floor` / `fast_round_ties_even` (pure SSE2, `cfg`-gated to x86-64) | `mic_distances` ortho 292 → 203 ms |
| 8-corner search as independent candidates + a 3-level tournament instead of a serial `if d < dmin` chain | `mic_distances` triclinic 571 → 411 ms |
| const-generic hoisting of loop-invariant flags, flat-slice reads, precomputed extended radii, guard-as-data | `get_mic_sasa` 611 → 359 ms (ortho), 1399 → 822 ms (tric); `get_mic_sasa_cell_list` tric 45.6 → 31.5 ms |

Net on the dense matrices: **1.46x orthogonal, 1.39x triclinic**; on the SASA family up to
**1.70x**. The durable rules extracted from this are now normative in
`devguide/rust_kernel_optimization_guide.md`, which also records the two benchmarks that
lied and the transformations that measured *worse*.

The method correction matters more than the numbers: §2 concluded "the margin is not inside
the kernels" from reading source. That was right about the arithmetic and wrong about the
lowering. For a kernel whose algorithm is already settled, the next question is what the
compiler emitted.

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
| C. Fused multi-observable passes | **closed as not worth doing** — the candidate pass measures ~2.5 ms, inside the surrounding Python's noise |
| D. SoA layout for SIMD | **closed as a negative result** — SoA is 0.94x / 0.69x vs AoS |
| E. Reduced cell for the triclinic MIC | done, and it fixed a correctness defect |
| F. SIMD instruction set / multiversioning | **closed** — baseline = v2 = v3 within noise once G landed; keep the portable wheel |
| G. What the compiler emitted (libm floor, serial reductions, loop-invariant branches) | done — 1.4-1.7x on the dense matrices and the SASA family; rules now in `devguide/rust_kernel_optimization_guide.md` |

No live items remain, which is why this document is archived. The work that continues lives
in `rust_numba_coexistence_and_cut_plan.md` (CI wheels, the crate's
permanent home, the Numba cut), `pending_proposals/rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`
(data model, now without its SIMD justification) and `rust_kernel_optimization_guide.md`
(normative method, plus the remaining per-kernel candidates in its section 9).

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
