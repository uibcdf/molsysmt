# Rust/Numba coexistence and the cut to Rust

**Status:** stages 1–2 implemented on `main` (2026-07-24); **default kernel is now `'auto'`**
(Rust where the wheel is importable, else Numba). Stage 3 (CI wheels) and the hard-`'rust'`
cut are open.
**Relates to:** `rusterization_pilot_conclusions_and_adoption.md`,
`linear_algebra_backend_for_rust_kernels.md`,
`rust_kernel_redesign_beyond_faithful_ports.md`, `rust_gpu_backend_options.md`,
`neighbor_list_consumer_migration.md`.
**Crate location:** `experiments/rust_kernels/` on `main` (the pilot branch
`experiment/rust-numba-pilot` is historical/superseded).

## Landing status (2026-07-24)

**Stage 1 — infrastructure — landed on `main`, inert by default:**

- The Rust crate source lives in `experiments/rust_kernels/` (path kept for continuity with
  the pilot docs; a permanent-home rename is a cosmetic follow-up).
- The dispatch seam `molsysmt/_private/rust_backend.py` is on `main`, with a guarded import
  so it is a no-op when the wheel is absent.
- `molsysmt.configure.kernel` (`'numba'|'rust'|'auto'`, default `'numba'`) plus the uniform
  per-call `kernel=` override are wired through `with_configure_overrides`.
- The seam reads `configure.kernel` when no explicit `backend=` is passed, and emits a
  single `DeprecationWarning` only on the *default* Numba path while a Rust wheel is
  present (explicit `backend='numba'`, used by tests and internal callers, stays quiet).
- The 166 Rust parity/property tests live at `tests/rust/` and pass.

Verified: `import molsysmt` is unchanged, a real `get_rmsd` call is byte-identical by
default, `configure.context(kernel='rust')` flips resolution and restores. **Main behaves
exactly as before** — nothing routes to Rust unless explicitly selected, and no public
function is wired to the seam yet.

**Stage 2 — consumer wiring — COMPLETE.** `configure.kernel='rust'` now takes effect
across the whole CPU analysis surface. Routing is at the *high-level consumers*, family by
family, each validated against its own test group on both backends: it could not be done by
replacing kernel names at module level, because several primitives (`dot_product`,
`get_distance_two_points`, the MIC/`math` helpers) are called *inside* other `njit` kernels
and rebinding those to a Python dispatcher breaks Numba compilation. Each consumer instead
calls the seam (`from molsysmt._private import rust_backend as _kernels`) instead of
`msmlib.structure.*`, honouring `configure.kernel` with no per-function argument. Consumers
that go through a *public* function (e.g. `center`, `move_away`, `align_principal_axes` via
`structure.get_center`) inherit the routing for free.

| family | consumers routed | tests (numba / rust) |
|---|---|---|
| RMSD | get_rmsd, get_least_rmsd, least_rmsd_fit, _native_placers | 20 / 20 |
| geometry | get_center, get_radius_of_gyration, get_rmsf, flip | 37 / 37 |
| axes + PCA | get_principal_axes, principal_component_analysis | 2 / 2 |
| angles + dihedrals | get_angles, get_dihedral_angles, set/shift_dihedral_angles | 11 / 11 |
| pbc | box geometry + wrap/unwrap + PDB handler | 52 / 52 |
| topology/series | component index, occurrence_order (convert path) | 22 / 22 |
| distances/neighbours/contacts | get_distances, get_neighbors, get_contacts | 88 / 88 |
| SASA | get_sasa (cell-list + brute-force), physchem.get_sasa | 16 / 16 |
| build (min-distance) | build_peptide | 148 / 148 |

Each pair agrees to the last bit end-to-end on the (small) test systems; on large systems
the agreement is at the documented scientific tolerance.

**CPU coverage is 100%.** After the first stage-2 pass the only ported-gap left was the
brute-force `get_sasa`/`get_mic_sasa` (small-system path) and the two `minimum_distance_*`
math kernels; those were then ported (`get_mic_sasa` corrects the same `_is_orthogonal`
typo as its cell-list sibling) and their consumers wired. The full Rust suite is 175 passed,
3 skipped.

**The one remaining exception, deliberate:** `_private/gpu.py` is the GPU dispatch,
orthogonal to the CPU numba/rust choice (`use_gpu` selects GPU; `kernel` selects the CPU
backend). GPU-from-Rust is its own decision — see `rust_gpu_backend_options.md`.

**What is left is no longer porting or wiring — it is the two open decisions:** stage 3 (CI
wheels) and the cut (when to flip the default and delete Numba). Both are gated on
dogfooding with `configure.kernel='rust'`, which is now possible across the whole surface.

**Default flipped to `'auto'` (2026-07-24), validated.** The full suite was run forcing
`configure.kernel='rust'` and compared against Numba: both give **9489 passes and the same
48 failures**, all pre-existing chemical-state/conversion WIP unrelated to the kernels
(no numerical/tolerance failure, no wired-kernel failure). Rust introduces zero regressions,
so `'auto'` is safe. `'auto'` (not hard `'rust'`) keeps the no-hard-dependency property:
Rust runs where the wheel is present, Numba otherwise.

**Stage 3 — CI wheels — not started.** Multiplatform `cp311-abi3` wheel builds are the gate
for a hard `'rust'` default; until then `'auto'` degrades gracefully where the wheel is absent.

## 0. Where we are

All 97 CPU `njit` kernels in `molsysmt.lib` have a Rust port in `experiments/rust_kernels/`
on `main` (69 Rust unit tests, 175 Python parity tests, 3 documented skips), reached
through the dispatch seam `molsysmt/_private/rust_backend.py`. The seam is wired into the
public analysis surface and reads `configure.kernel`; when the Rust wheel is absent, or
`configure.kernel='numba'` (the default), it is a no-op and MolSysMT behaves exactly as
before — the import is guarded, so there is **no hard dependency and no 1.0 debt**. The
remaining work is not porting or wiring — it is the two decisions below: CI wheels, and the
cut (flip the default, retire Numba), both gated on dogfooding.

## 1. The mechanism: reuse `configure`, do not add per-function arguments

MolSysMT already has the exact pattern this needs. `molsysmt.configure` holds global
options (`parallel_mode`, `num_threads`, `precision`, `cell_list`, …), and every
`configure`-wrapped function accepts uniform per-call overrides (`parallel=`,
`num_threads=`, …) funnelled into a per-call context. Kernel selection must use the same
mechanism, not a bespoke argument threaded through 97 signatures:

- **Global:** `configure.kernel = 'rust' | 'numba' | 'auto'`.
- **Per-call override:** a uniform `kernel=` keyword, digested by the existing wrapper.

This also settles a question raised during the PCA work: parallelism (`Par::rayon` vs
`Par::Seq` in faer, `prange` gating in Numba) is **not** a per-kernel decision either. The
Rust kernels must read `configure.parallel_mode` / `configure.num_threads` — the pilot
hardcodes "all cores" as a placeholder and must not ship that way.

## 2. The real gate is packaging, not code

The pilot's whole value is that `molsysmt` does not import the crate, so nothing here
touches 1.0. Making Rust reachable by default reverses that, and the decision underneath
"default `'rust'`" is: **what happens when the wheel is absent?**

- **Hard dependency** — the Rust wheel becomes a required install. Needs CI producing
  `cp311-abi3` wheels for every target platform (Linux x86_64/aarch64, macOS
  x86_64/arm64, Windows x86_64). This is a genuine 1.0 infrastructure commitment.
- **Graceful `'auto'`** — Rust when the wheel imports, Numba otherwise. No hard dependency,
  no install-time failure, but "default rust" is then aspirational rather than guaranteed.

Recommendation: **`'auto'` as the shipped default during dogfooding**, flipping to a hard
`'rust'` default only once wheels are proven on all target platforms. This keeps the
no-debt property until the infrastructure actually exists to back a hard default.

The single-wheel, no-BLAS-dependency property (see
`linear_algebra_backend_for_rust_kernels.md`) is what keeps this tractable: one
`cp311-abi3` wheel per platform, pure Rust, `faer`/`nalgebra` rather than a system LAPACK.

## 3. The numerical change is real and must be announced

Parity with Numba is at **tolerance, not bit-for-bit**, and unavoidably so: `fastmath`
(FMA and reassociation), different eigensolvers, and pairwise-vs-sequential summation all
move the last bits (~1e-15 to ~1e-9 depending on the kernel; see the block-9/13 notes).
Making Rust the default therefore changes MolSysMT's numerical output at that level.

- Downstream reference values and pinned tests (topomt, pharmacophoremt, elasnetmt,
  pocketmt-tools, and MolSysMT's own fixtures) may notice. Dogfooding is exactly the
  mechanism to surface this before it reaches users.
- Three kernels *deliberately* diverge (documented, tested, reported):
  `wrap_to_mic` (minimum image on triclinic boxes), `set_mic_dihedral_angles` (broadcast),
  and the principal-axes sign convention. On those, Rust is the *more* correct answer —
  see the `pending_bugs/` reports.

## 4. Deprecation policy

- In **1.0**: selecting `kernel='numba'` (or falling back to it) emits a
  `DeprecationWarning` naming the removal target. Numba stays fully functional.
- **Post-1.0**, once dogfooding has surfaced no blocker: delete the Numba kernels, drop the
  `kernel=`/`configure.kernel` switch, and make Rust unconditional. Retire the parity test
  layer (its job is done) but **keep the property tests** — they outlive the oracle.

Deleting Numba also removes the whole `lazy_njit`/`parallel_mode`/`parallel_threshold`
machinery and the open `parallel_numba_jit_segfault` bug class. That simplification is a
large part of the payoff and should not be left half-done: **maintaining both
implementations forever is the worst outcome** — all of the duplication cost, none of the
simplification.

## 5. Sequencing (this is the answer to "what before, what after")

**Independent of this plan — can proceed now:**

- **Redesign lever A (PCA covariance):** already done, inside the Rust PCA port.
- **Redesign lever B (route `get_contacts`/`get_neighbors` through the cell-list
  primitive):** a `molsysmt`-level dispatch change that improves the **Numba** path too, so
  it is not part of the cut at all. Already scoped in `neighbor_list_consumer_migration.md`.
  Do it on its own merits; it is the largest measured win on real workloads
  (`get_contacts` on a trajectory currently builds the dense distance matrix — 2.7 s).

**The plan itself, in order:**

1. Land this plan and the packaging decision (§2) toward `main`. Decide hard-dep vs auto.
2. Wire the crate into the build behind an optional import; stand up CI wheels.
3. Add `configure.kernel` + the uniform `kernel=` override (§1); wire faer/Numba
   parallelism to `configure` (§1).
4. Ship with `kernel='auto'` default; add the `DeprecationWarning` on Numba selection (§4).
5. Dogfood to 1.0. Watch for numerical drift (§3) and any correctness surprise.
6. Flip the default to `'rust'` once wheels are proven.

**After the cut (post-1.0), not before:**

- **Redesign lever C** (fused multi-observable passes). Measured negligible so far; keep it
  open but unprioritised. While Numba is the oracle it pays the parity tax twice; once Rust
  is the implementation it becomes ordinary work behind the property tests.
- **Redesign lever F** (SIMD instruction set / multiversioning) is **closed, measured, no
  action**: after the lowering fixes below, the baseline, `x86-64-v2` and `x86-64-v3` builds
  are equal within noise on every kernel measured. Keep the single portable baseline wheel;
  the earlier apparent AVX2 gains and the dense-distance regression were both artifacts of
  how `f64::floor` was lowered, not of vector width.

  **Resolved and no longer post-cut work:** lever D (columnar/SoA SIMD layout) is closed as a
  *negative* result — SoA measured 0.94x baseline and 0.69x under AVX2 against the current AoS
  layout. Lever E (reduced cell for the triclinic MIC) was pulled forward and is done, because
  it was also a correctness fix. Lever G (what the compiler actually emitted: libm `floor`
  calls in the innermost loops, a serial reduction in the 8-corner wrap, loop-invariant
  branches) is done and bought 1.4-1.7x on the dense distance matrices and the SASA family;
  its durable rules are normative in `devguide/rust_kernel_optimization_guide.md`.

  All of the above: see `rust_kernel_redesign_beyond_faithful_ports.md`.

## 6. What this explicitly does not do

- It does not make the cut a 1.0 blocker. If wheels are not ready, ship `'auto'`; the
  no-debt property holds and the flip waits.
- It does not touch the public numerical contract silently: the tolerance-level change is
  announced and dogfooded, and the three deliberate divergences are documented bugs where
  Rust is the correction.
