# Rusterization pilot — conclusions and adoption path

**Status:** **HISTORICAL PILOT EVIDENCE — the adoption question it asked is settled
(archived 2026-07-28).**
**Relates to:** `rusterization_heavy_computations.md`,
`../../pending_proposals/rusterization_topology_and_selections.md`,
`../../pending_proposals/rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`,
`../../pending_proposals/rusterization_parallel_trajectory_io.md`.
**Pilot location (historical):** branch `experiment/rust-numba-pilot`, dir
`experiments/rust_kernels/`. Neither exists on `main` any more: the production crate
lives at `rust/` and ships as the private `molsysmt._rust` extension.

> ## Why this is archived
>
> This document asked whether MolSysMT should adopt Rust, and on what terms. The
> answer landed in full: all 97 CPU kernels are ported, Numba is removed (Segment D),
> the crate is packaged as an abi3 wheel across five native targets (Segment C), and
> the result is validated (Segment E). See
> [`release_1_0_status.md`](../../release_1_0_status.md).
>
> Its **measurements remain useful** as the record of what the pilot found and why
> the decision went the way it did. Its **recommendations do not apply**: the
> proposal to keep wheel infrastructure until after 1.0 and ship Numba as the 1.0
> fallback was superseded by the maintainer decision of 2026-07-26, and both halves
> of that recommendation are now contradicted by shipped work.
>
> For how the ported kernels are made fast, see
> [`rust_kernel_optimization_guide.md`](../../rust_kernel_optimization_guide.md).

## 1. What was tested

A real Rust extension (PyO3 + rust-numpy, built with maturin) reimplementing several
kernels across different computational profiles, benchmarked against their Python/Numba
equivalents, plus a real production kernel and the packaging/opt-in questions.

## 2. Evidence

Parity was **exact (bit-for-bit)** in every kernel tested at the time of this pilot,
including a production kernel compiled with Numba `fastmath=True`.

> **Superseded in part (2026-07-24, blocks 9 and 10).** That result does not generalise.
> `lazy_njit` sets `fastmath=True`, which lets LLVM contract three-term dot products into
> FMAs and vectorise long accumulation loops into partial sums; Rust does neither by
> default. Wherever a kernel contains such a reduction the two disagree at ~1e-15, and no
> amount of care on the Rust side closes it. This was verified, not inferred: rebuilding
> the same kernels with `fastmath=False` reproduces the Rust results exactly (0 differing
> elements), and the fastmath-vs-no-fastmath divergence count matches the Rust-vs-Numba
> one element for element. The pilot's kernels happened to give fastmath nothing to
> exploit. **Bit-for-bit parity is therefore an outcome, not a gate the migration can rest
> on**; the affected kernels are gated at a documented scientific tolerance instead. See
> `linear_algebra_backend_for_rust_kernels.md`, which depends on this correction.

| Axis | Finding |
|---|---|
| Warm — idealized tight loops (pairwise sqdist, Coulomb) | **tie** (Numba already at C speed) |
| Warm — real production kernel (`get_mic_distances_single_system`, N=1488) | **14× orthogonal, 27× triclinic** |
| Cold (first call) | **26–266×** (Numba JITs per kernel; a complex kernel cost 3.4 s to compile) |
| Parallel (rayon vs `numba prange`, 20 threads) | rayon ≥ Numba (6.4× vs 5.5×), no `parallel_mode`/`parallel_threshold` gating, no segfault class |
| Branchy/irregular (cell-list counts) | Rust ~15% faster warm |

**The decisive correction:** the "warm is a tie" result holds only for idealized loops.
The *production* kernel is written naturally (`np.empty((3))` per pair, nested njit calls
`wrap_to_mic`→`norm`, array slicing); Numba does not remove that allocation/call overhead,
while the Rust port uses stack arrays (`[f64;3]`, zero heap). So on real, readably-written
kernels Rust is dramatically faster warm as well. Honest caveat: a hand-optimised Numba
(pre-allocated scratch, manual inlining) would narrow the warm gap — part of the win is
"Rust vs naturally-written Numba". The maintainability argument stands: Rust delivers
optimal performance from readable code, for free.

## 3. Packaging is not a technical unknown any more

- A single **`cp311-abi3`** wheel was built and **runs on Python 3.11–3.13** (verified by
  installing the cp311-abi3 wheel and running it on 3.13). `rust-numpy` works under abi3.
- Binary wheels mean **no user-side compilation and no warmup**: the compile happens once
  in CI; `pip install` downloads a prebuilt `.so`. Compile-at-install only happens as an
  sdist fallback when no wheel matches (needs Rust on the user's machine — to avoid).
- CI cost: 5 build legs `(os × arch)` with abi3 (not `× python-version`), standard via
  `PyO3/maturin-action`. See `experiments/rust_kernels/ci/build-wheels.skeleton.yml` and
  `PACKAGING.md`.
- The opt-in seam (`try import msm_rust_kernels`, `backend='auto'|'rust'|'numba'`, Numba as
  oracle) is trivial and safe — see `experiments/rust_kernels/fallback_seam.py`.

## 4. Verdict

Rust is a credible substantial unlock, but **not as "faster math"** — it is:
- **instant start** (no JIT / no `warmup()`), which *compounds* across the ~107 njit sites;
- **robust** (removes the Numba-parallel segfault class and the `parallel_mode` gating dance);
- **parallel-safe** (rayon);
- with a **real warm win on production-style kernels** and an edge on irregular graph/spatial
  algorithms — exactly the direction of the columnar/CSR/BVH engine
  (`rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`).

There is no remaining technical blocker. What remains is a **strategic/resourcing decision**:
take on a second toolchain and multi-OS wheel CI.

## 5. Updated Adoption Boundary

The modular migration described by the original pilot has been completed for
the recorded CPU surface: all 97 kernels have Rust counterparts and their
high-level consumers are routed through the transition seam.

The remaining adoption work is now pre-1.0:

1. restore the unrelated conversion-fidelity baseline;
2. freeze and record Numba as the final temporary oracle;
3. productize and test multiplatform Rust wheels;
4. remove CPU Numba, Numba-CUDA, backend selection, warmup, diagnostics, and
   dependencies;
5. validate the Rust-only installed product and direct MolSysSuite consumers.

The coexistence cost is accepted only for that bounded migration interval.
There will be no permanent Numba fallback in MolSysMT 1.0.

## 6. Target Selection Outcome

The pilot's original target-selection guidance has completed its purpose.
Complex MIC, allocation-heavy geometry, irregular neighbor, SASA, topology,
series, PCA, and the remaining CPU families have all been ported. New work must
focus on packaging, independent scientific evidence, removal completeness, and
installed-product behavior rather than selecting more Numba kernels to port.

## 7. Recommended Immediate Step

Follow Segments A–C of
[`release_1_0_execution_plan.md`](../../pending_proposals/release_1_0_execution_plan.md): first restore
conversion-fidelity coherence, then capture the final oracle inventory, move the
crate out of `experiments/`, and turn the wheel skeleton into real
multiplatform installed-wheel CI. Numba deletion begins only after that
packaging gate passes.
