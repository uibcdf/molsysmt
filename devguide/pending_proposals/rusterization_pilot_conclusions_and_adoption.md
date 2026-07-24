# Rusterization pilot — conclusions and adoption path

**Status:** evidence-based recommendation (2026-07-24). Consolidates a hands-on pilot.
**Relates to:** `rusterization_heavy_computations.md`, `rusterization_topology_and_selections.md`,
`rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`, `rusterization_parallel_trajectory_io.md`.
**Pilot location:** branch `experiment/rust-numba-pilot`, dir `experiments/rust_kernels/`
(self-contained PyO3 crate; not wired into the molsysmt build; molsysmt never imports it).

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

## 5. Adoption path — and the 1.0 boundary

The migration is **modular**: each kernel moves independently behind the opt-in seam, with the
Numba kernel kept as oracle and a per-kernel parity test. Every migrated kernel is banked.

**Separate two decisions, and keep them off the 1.0 critical path:**

1. **Migrate kernels to Rust (the code).** Bankable, low-risk, can start now. Each kernel
   lives behind `backend='auto'` with **Numba as the default/fallback**, so 1.0 ships exactly
   as it would without Rust (pure Numba, no new packaging blocker). Pre-1.0 work here is
   genuinely *trabajo ganado*.
2. **Ship Rust wheels in the distribution (the infrastructure).** Standing up the multi-OS
   wheel CI + committing to a second toolchain. This is the bigger commitment and should be a
   **post-1.0** decision — it must NOT become a 1.0 release blocker.

Consequence of the split: pre-1.0 Rust kernels are *banked capability* (they run when the
wheel is present), but the user-facing benefit (no warmup, dropping the Numba dependency)
only lands once Rust ships as the default — i.e. after decision 2. That is fine and expected.

**Carrying cost to accept:** during the transition each migrated kernel means two
implementations (Rust + Numba) kept in lockstep by a parity gate. Numba stays until Rust is
shipped and trusted.

## 6. Suggested first targets (highest value/effort)

Prefer kernels that maximise the cold+warm win and the maintainability payoff:
- **complex kernels with expensive JIT** (biggest cold cost) — e.g. the MIC distance family
  (`get_mic_distances*`), already piloted with exact parity;
- **allocation-heavy / nested-call kernels** written in the natural per-element style (biggest
  warm win, as shown);
- **irregular/graph/spatial** kernels (cell lists, covalent-graph traversals, selections) —
  they gain most and align with the columnar-engine direction.

Avoid, for now: kernels that are already tight, well-vectorised loops (warm tie — low return),
and anything touching the CUDA path (out of scope; keep Numba there).

## 7. Recommended immediate step (if adopted)

Turn the pilot crate into a proper, still-optional package skeleton on a feature branch:
one real kernel migrated behind the seam with a parity test wired into the suite, plus the
wheel-CI skeleton promoted to a real (manually-triggered) workflow — WITHOUT making 1.0 depend
on it. That validates the end-to-end developer loop (edit Rust → parity test → optional wheel)
before scaling to more kernels.
