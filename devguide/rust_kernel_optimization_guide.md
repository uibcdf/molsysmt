# Optimising the Rust kernels

**Role:** operational. This is the working method for making `rust/`
fast without making it wrong. It records what was *measured* on this codebase — including
the things that turned out not to work — so the same ground is not re-explored.

**Scope:** the Rust CPU kernels. It does not cover the retired pre-1.0 CPU/GPU
experiments. For where redesign effort should go at the *algorithm* level,
see `archive/resolved_proposals/rust_kernel_redesign_beyond_faithful_ports.md`; this document is
about the layer below that, once the algorithm is settled.

## 0. The rule that produced everything below

**Measure, then change. Read the emitted assembly before concluding a loop is optimal.**

On this codebase, source-level speculation about kernel performance had a hit rate of about
1 in 3. Every real win here was found either by a differential benchmark or by
`objdump`-ing the built `.so` — never by reading Rust and reasoning about it. Two of the
findings are things no amount of source reading could have surfaced, because they are
properties of the *lowering*, not of the code.

Corollary: a benchmark you have not tried to invalidate is not evidence. Two benchmarks
written during this work were wrong in opposite directions — see §5.

**Before choosing what to optimise, read §10.** It carries the end-to-end profile (which
operations actually dominate), the two costs that live outside any kernel, and the three
kernels that are already optimal — inherited measurements that save re-deriving them.

## 1. Know what the baseline target actually has

The wheel is built for the **x86-64 baseline** (SSE2) so that one portable artifact runs
everywhere. That decision is deliberate (see §6) but it has a consequence that dominated the
hottest kernel in the library:

**On x86-64 baseline there is no floor, ceil, trunc or round-to-nearest instruction.**
`roundsd` is SSE4.1. So `f64::floor()` and `f64::round_ties_even()` lower to an *indirect
call into libm*.

The minimum-image wrap does three floors per displacement vector. In
`get_mic_distances_single_system` that is three libm calls in the innermost loop of an
O(N²) kernel — visible in the disassembly as `call *%rax` between the arithmetic:

```
2cc12a:  divsd  0x1b0(%rsp),%xmm0
2cc13b:  addsd  %xmm1,%xmm0
2cc146:  call   *%rax              <-- floor
...
2cc168:  call   *0xee0ca(%rip)     <-- floor
...
2cc1a5:  call   *%rax              <-- floor
2cc1f2:  sqrtsd %xmm0,%xmm0
```

A call in the loop body also makes the loop **unvectorisable**, so the cost is not just the
calls: the whole body stays scalar.

`mathlib::fast_floor` and `mathlib::fast_round_ties_even` replace them with pure SSE2
arithmetic (truncate-and-correct; add-magic-number), each **bit-identical** to the intrinsic
on the domain these kernels use, each verified against the intrinsic over a 600k-value sweep
plus the awkward fixed cases (`-0.0`, exact halves, `2^51`, `1e300`). A lint keeps them
from coming back — see §7.

Measured effect on `mic_distances` (n = 4000, one structure), orthogonal box:
**292 ms → 203 ms**, from this change alone.

Note the asymmetry with Numba, which is *not* a Rust deficiency but a JIT/AOT difference:
Numba compiles through llvmlite for the **host** CPU (`broadwell` on this machine), so its
`np.floor` was always a single `roundsd`. Comparing an AOT baseline build against a
host-tuned JIT is not comparing languages.

**Both helpers are `cfg(target_arch = "x86_64")`.** AArch64's base ISA has `frintm`, so
`floor` is already one instruction there and the arithmetic version would only add work.
This is an ISA-gap fix, not a universal trick — check any new target the same way.

## 2. Universal transformations (these hold on any modern out-of-order CPU)

Unlike §1, the following are about cache lines, store queues and dependency chains, which
every current CPU has. They transfer across architectures.

### 2.1 Hoist loop-invariant branches out with const generics

A flag that comes from the box or the call arguments is loop-invariant, but as a runtime
`bool` it leaves a branch in the innermost loop and blocks vectorisation. Monomorphise:

```rust
if ortho { f::<true>(..) } else { f::<false>(..) }
```

Applied to `mic::mic_vector_const<ORTHO>`, `mic::fill_mic_upper<ORTHO>`,
`sasa::atom_sasa<WRAP, ORTHO>`. The `Option<(&Mat3, &Mat3, bool)>` that the SASA occlusion
loop used to test per candidate is the same defect in another shape.

### 2.2 Never scatter-store inside the pair loop

Filling an `n x n` symmetric matrix by storing `out[j][k]` **and** `out[k][j]` per pair
makes the second store a column walk (stride `n * 8` bytes) and, worse, prevents any vector
store. `symmetric::mirror_upper_to_lower` fills the strict upper triangle with unit-stride
stores and mirrors afterwards in a cache-blocked pass.

**This one is conditional, and the condition is measurable**: the mirror pass is a second
sweep over the whole matrix, a fixed cost that only pays when the per-pair arithmetic is
cheap enough for the store pattern to matter (n = 4000):

| | mirror store per pair | upper triangle + mirror pass |
|---|---|---|
| non-periodic `distances` | 367 ms | **281 ms** |
| MIC, orthogonal box | 230 ms | **201 ms** |
| MIC, triclinic box | **388 ms** | 409 ms |

So `mic::fill_mic_self` splits for the orthogonal path and keeps the stores interleaved for
the triclinic one. Do not apply this transformation blind; benchmark the specific kernel.

### 2.3 Break serial dependency chains

A `for .. { if d < dmin { dmin = d; best = r; } }` scan is *latency* bound: every iteration
waits on the previous compare-and-select. The reduced-cell wrap's 8-corner search was the
dominant cost of every triclinic MIC kernel at ~60 ns per pair.

Rewritten as eight independent candidates plus a three-level tournament
(`wrap_to_mic_vector_reduced`): **571 ms → 411 ms** on `mic_distances`, and bit-identical —
each `d` is the same expression and each pairing keeps the lower index, which reproduces the
scan's "first minimum wins" tie-breaking exactly.

When restructuring a reduction, state explicitly in the code why it is still bit-identical,
or accept and document that it is not.

### 2.4 Read through flat slices, not `ArrayView` indexing

`c[[s, k, 0]]` recomputes `sum(stride_i * idx_i)` and bounds-checks on every access. In an
O(N²) body that is a measurable fraction, and it is enough on its own to stop the
vectoriser. Take the slice once:

```rust
let cc = c.as_standard_layout();          // borrows when already C-contiguous
let cs = cc.as_slice().expect("standard layout is contiguous");
```

`as_standard_layout` returns a `CowArray`, so a non-contiguous input stays correct at the
cost of one copy. Do **not** hand-roll a `(&[f64], Option<Array>)` helper for this: it is
self-referential and unsound.

### 2.5 Hoist per-iteration recomputation into a precomputed table — and turn guards into data

The SASA occlusion loop recomputed `radii[ll] + probe` and its square once per
(sphere point, candidate) instead of once per atom. `sasa::extended_radii_sq` precomputes
the squares, and stores `0.0` for non-positive radii so that the `d2 < rext2[ll]` test
rejects them for free — the `if r_l_ext <= probe { continue; }` guard becomes data rather
than a branch, provably equivalently, since `d2` is a sum of squares.

With §2.1 and §2.4, on the SASA family: `get_mic_sasa` **611 → 359 ms** (orthogonal) and
**1399 → 822 ms** (triclinic); `get_mic_sasa_cell_list` triclinic **45.6 → 31.5 ms**.

## 3. What did *not* work

Recorded so it is not attempted again.

- **Columnar (SoA) coordinates for SIMD.** Measured *slower* than the current AoS `[n, 3]`:
  0.94x on the baseline build and 0.69x under AVX2. A pair kernel reads one cache line per
  atom with AoS and three separate streams with SoA. Vectorisation widens the gap.
- **A fixed AVX2 (`x86-64-v3`) build.** Once §1 removed the libm calls, baseline ≈ v2 ≈ v3
  within noise (§6). Before §1 it looked like a 1.1-1.3x win on some kernels and a 16-25%
  *regression* on dense distances — both artifacts of how `floor` was being lowered.
- **Cache-blocking the interleaved mirror store** (tiling so `out[k][j]` stays resident).
  Marginal on the orthogonal path (253 vs 270 ms) and *worse* on the triclinic one; §2.2's
  deferred pass is the better shape where a change is warranted at all.
- **An extra `t == 0.0` select in `fast_floor`** to get `-0.0` exactly right. It cost the
  entire vectorisation gain (203 → 278 ms). `copysign` is the branch-free way to do it.

## 4. Correctness discipline

The optimisations above are only acceptable because the kernels are covered first:

- **80 `cargo test` unit tests** (`cargo test --no-default-features -q`) and **262 Python
  tests** in `tests/rust/`, including `test_mic_neighbors_battery.py` — 11 box shapes,
  several cutoffs, ground truth from an independent all-pairs ±2/±3 search.
- Optimise only behind that net, never before it. The MIC and neighbour battery was written
  *first*, deliberately, and it is what made this work safe.
- State for every change whether it is bit-identical or not, and why. Prefer bit-identical.
  When a change cannot be (e.g. an algebraically rearranged reduction), say so in the code
  and validate against the independent oracle rather than against the previous version.
- Re-run the public-API tests too, not just the kernel tests: `tests/rust tests/pbc
  tests/physchem tests/structure tests/lib` (603 tests) exercise these kernels through
  the production Rust adapter.

## 5. Two benchmarks that lied

Both were caught; both are the reason §0 says to try to invalidate your own measurement.

1. **A branch-free SoA/AoS comparison reported AoS at 0.0 ms.** LLVM proved the accumulator
   unused and deleted the loop. Any "impossibly fast" result is a dead-code result. Keep a
   consumed output (a checksum) and assert on it.
2. **A standalone replica of the MIC kernel showed a 1.56x win that the real kernel did not
   reproduce.** In the replica the variants were driven by a `for (..) in [array literal]`
   loop, which LLVM unrolled — making the `ortho` flag a *compile-time constant* and
   enabling an optimisation the real kernel (runtime flag) could not get. The chase for that
   discrepancy is what found §2.1. `std::hint::black_box` the *data*; also check that
   control-flow parameters are not being constant-folded.

A third habit worth keeping: when a microbenchmark and the real kernel disagree, the
microbenchmark is wrong until proven otherwise, and the disagreement is usually informative.

## 6. Distribution: instruction sets and multiversioning

The crate builds with `opt-level = 3`, `lto = true` and **deliberately no `target-cpu`**;
`Cargo.toml` says why at the profile.

Measured after §1-§2, same sources, three microarchitecture levels:

| kernel (n = 4000) | baseline | `x86-64-v2` | `x86-64-v3` (AVX2+FMA) |
|---|---|---|---|
| `mic_distances` orthogonal | 200.9 ms | 199.6 ms | 198.1 ms |
| `mic_distances` triclinic | 409.3 ms | 437.5 ms | 401.4 ms |
| `distances` orthogonal | 281.3 ms | 287.2 ms | 288.9 ms |
| `neighbor_list` 50 x 2000 | 17.9 / 19.1 ms | 16.5 / 17.5 ms | 17.7 / 19.0 ms |
| `sasa_cell_list` | 21.2 / 35.6 ms | 19.9 / 33.5 ms | 19.7 / 35.3 ms |

**All within noise.** Once the hot loops stop calling libm, the instruction set stops
mattering for these kernels — they are limited by dependency chains and memory traffic, not
by vector width.

Therefore:

- **Keep the portable baseline wheel.** It is not leaving measurable performance behind.
- **Runtime multiversioning is not worth doing** for these kernels. It would be the *right
  mechanism* if a win existed — one portable wheel, per-function clones dispatched on
  `is_x86_feature_detected!`, which is what numpy and the BLAS libraries do, and no user
  compiles anything — but there is currently nothing for it to win. Revisit only if a
  specific kernel's own benchmark shows a gap, and then multiversion *that* kernel, never
  the whole crate.
- **Never ship a fixed `x86-64-v3` baseline.** It gains nothing here and turns every
  pre-AVX2 CPU into an `ILLEGAL_INSTRUCTION` crash at import.
- Building from source with `-C target-cpu=native` stays available to anyone tuning a
  cluster; it is not a path users should need.

Note the interaction between §1 and multiversioning: inside an SSE4.1-or-better clone,
`f64::floor` *is* one instruction, so `fast_floor` would be unnecessary there. The
arithmetic version is what makes the single portable wheel as fast as a tuned one — which is
precisely why multiversioning has nothing left to add.

## 7. What is automated, and what is not

Be clear about this, because the tests are green either way.

**Automated:**

- **Correctness.** 80 `cargo test` tests + 262 Python tests in `tests/rust/`, with independent
  oracles. A wrong optimisation fails loudly.
- **The libm-rounding regression class.**
  `devtools/scripts/check_rust_hot_paths.py` fails if `.floor()` / `.ceil()` / `.round()` /
  `.round_ties_even()` / `.trunc()` reaches production kernel code without an explicit
  `// libm-ok: <reason>` marker. It runs in `devtools/scripts/release_gate.py` and in
  `tests/rust/test_hot_path_lint.py`. That test file has **two** tests: the lint passes, and
  the lint *fails* on a tree where the regression has been planted — a guard that cannot fail
  is worthless, so it is itself guarded. Verified: reintroducing one `.floor()` in the
  orthogonal wrap is caught.

**Not automated — and these are the ones to be honest about:**

- **Performance itself.** Nothing measures whether a kernel got slower. A change that
  reintroduces a scattered store (§2.2), a runtime flag in an inner loop (§2.1), an
  `ArrayView` index in a hot body (§2.4) or a serial reduction (§2.3) will be silently
  accepted. Those patterns are too context-dependent for a lint: each is *correct* in cold
  code, and §2.2 measured *worse* on one of the two paths it was applied to.
- **The benchmark scripts are manual.** `bench_production.py`, `bench_neighbors.py`,
  `bench_matrix.py` and the ad-hoc scripts used here are run by hand; there is no recorded
  baseline and no comparison. Building a *credible* automated gate is a separate piece of
  work, already scoped in
  `pending_proposals/benchmark_regression_gate_reliability.md` — the hard part is statistical
  credibility on noisy hardware, not the plumbing.
- **The disassembly step (§0, §6, checklist item 4) is a human activity.** It is what found
  the largest win, and there is no substitute for it yet.

So: the method in this document is a *method*, not a mechanism. Until a benchmark gate
exists, the discipline is procedural — the checklist below, applied deliberately.

## 8. Checklist for a new or suspect kernel

1. Is the algorithm right? (Complexity; the levers already decided are in `archive/resolved_proposals/rust_kernel_redesign_beyond_faithful_ports.md`.) Stop here if not.
2. Is it covered by tests with an *independent* oracle? Write them first.
3. Benchmark it. Record the input shape; keep the script.
4. `objdump -d` the built `.so`, find the function, look at the inner loop for: `call`
   (libm — §1), only `-sd` scalar forms and no `-pd` packed ones, and a long chain of
   dependent `minsd`/select (§2.3).
5. Check the loop body for: loop-invariant branches (§2.1), scattered stores (§2.2),
   `ArrayView` indexing (§2.4), recomputed invariants and guard branches (§2.5).
6. Change one thing at a time and re-measure. Confirm bit-identity or document its loss.
7. Re-run both test layers before believing the number.

## 9. Remaining candidates, and why they are not urgent

State as of 2026-07-26, after the O(N²) matrices and the SASA family were done. Recorded
here rather than in a proposal so it survives that proposal's archival.

**Swept and clean.** Every `.floor()`/`.round()` left in the crate is either a `#[cfg(test)]`
ground-truth oracle, `reduce_cell` (once per box), or a synthetic bench probe in `lib.rs` —
all marked `// libm-ok:` and enforced by the lint in §7. There is no remaining instance of
the §1 defect.

**Not yet examined, ranked by remaining `ArrayView` indexing in loop bodies:** `rmsd.rs`
(29 sites), `geometry.rs` (26), `dihedral_ops.rs` (17), `axes.rs` (15).

**Why they are low priority, on evidence rather than intuition:** these are O(N) or O(N·S)
sweeps, not O(N²) kernels. `get_center`, `get_radius_of_gyration` and `get_rmsf` each came
out a *tie* against Numba in the original block-10 benchmark precisely because they are
memory-bound — the arithmetic is trivial and the cost is reading the coordinates. The
corroborating measurement from this round is `neighbor_list`, which moved only 1.08-1.17x
from the same treatment because its cost is the candidate *gather*, not the arithmetic.
Expect single-digit percentages here, not the 1.4-1.7x the dense matrices gave.

**So:** do not sweep them mechanically. If one of them shows up in a real profile, apply the
§8 checklist to that kernel alone and keep the benchmark.

**Closed as not worth doing:** fusing the multi-observable trajectory passes (a "compute
these observables in one sweep" API, so the trajectory is read once instead of three times).
Measured: the candidate pass is ~2.5 ms, so the saving is inside the noise of the surrounding
Python. It was the last live item of
`archive/resolved_proposals/rust_kernel_redesign_beyond_faithful_ports.md` (lever C) and it
is recorded here because the idea is plausible enough to be re-proposed.

## 10. Inherited measurements worth not re-deriving

These come from the (now archived)
`archive/resolved_proposals/rust_kernel_redesign_beyond_faithful_ports.md` and are duplicated
here deliberately: they are the facts a developer needs in order to *choose* what to optimise,
and they must not be reachable only from an archived file.

### 10.1 Where the time actually goes

End-to-end profile of real MolSysMT calls — TcTIM, 3983 atoms, 1 structure; pentalanine
trajectory, 62 atoms, 5000 structures — warm (JIT already compiled), **as measured before
this round of optimisation**:

| operation | warm wall clock |
|---|---|
| `get_contacts` (trajectory, 5000 structures) | 2732 ms |
| `get_sasa` (protein) | 628 ms |
| `get_contacts` (protein Cα, threshold) | 493 ms |
| `get_rmsd` / `get_least_rmsd` / `get_radius_of_gyration` (traj) | ~255 ms each |
| `get_center` (protein) | 236 ms |
| `get_neighbors` (protein Cα, threshold) | 18 ms |

The absolute numbers are stale — the dense matrices and the SASA family have since improved
1.4-1.7x (§1-§2), and `get_contacts` was rerouted through the cell list. **The ranking is the
durable part**: contact/distance queries over trajectories dominate, SASA is second, and
everything else is an order of magnitude down. Re-profile before trusting any of it, but start
from this order.

### 10.2 The two costs that are not in any kernel

1. **`get_contacts` on a trajectory was materialising the full dense N×N distance matrix per
   structure and then thresholding** — 2.3 s of its 2.9 s — when a contact query only needs
   the pairs under the threshold. Fixed by routing through the cell-list primitive; the
   threshold now sits at **> 400 atoms** in `molsysmt/structure/get_contacts.py`, with the
   crossover measured near 500. If you touch that constant, re-measure the crossover.
2. **`gc.collect` is a first-class cost.** In the mixed profile it was **1.8 s of 5.0 s**; in
   `get_contacts` alone, 0.48 s — the Python garbage collector tracing the per-operation
   temporaries the naturally-written Numba allocates. The Rust ports remove that pressure by
   doing arithmetic on the stack (verified: 50 `get_rmsd` calls, 47 KB input, 4.2 KB
   Python-side peak; `PyReadonlyArray` borrows numpy's buffer and `wrap_to_pbc` mutates in
   place at the same address). Keep it that way: a Rust kernel that allocates per call gives
   back one of the migration's main wins, and no benchmark of the kernel alone will show it.

### 10.3 Three kernels that are already optimal — do not "discover" them again

Checked, and already present in the *original* Numba (so also in the ports):

- the self-distance matrix already iterates `kk in range(jj+1, n)` and mirrors, so it does
  N(N-1)/2 work, not N²;
- the SASA occlusion loop already `break`s as soon as a sphere point is occluded;
- `get_distances` already exploits symmetry.

Speculation about in-kernel wins had a hit rate of 1 in 3 partly because of these.

### 10.4 PCA: the covariance, not the eigensolver

`principal_component_analysis` spent 76-93% of its time *building* the covariance matrix, not
diagonalising it, and the build was a mis-transcribed matrix product: `X.T @ X` is **48-132x
faster** than the triple loop. This is why the crate uses pure Rust (`nalgebra` for 3x3/4x4,
`faer` for large dense) instead of taking a LAPACK/MKL system dependency — the useful property
was fast BLAS, not a fast eigensolver. Full argument:
`pending_proposals/linear_algebra_backend_for_rust_kernels.md`.

### 10.5 The framing

"Can the kernels be more optimal if we escape the transported code?" — yes, but the win is
almost never in *what arithmetic a kernel does*. It is in choosing a different algorithm at
the dispatch level, a different API shape, recognising what an operation actually is, or —
the one this document exists for — in what the compiler emitted for a loop whose algorithm
was already right.
