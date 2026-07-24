# Rust/Numba coexistence and the cut to Rust

**Status:** migration plan (2026-07-24), pending decision to start.
**Relates to:** `rusterization_pilot_conclusions_and_adoption.md`,
`linear_algebra_backend_for_rust_kernels.md`,
`rust_kernel_redesign_beyond_faithful_ports.md`,
`neighbor_list_consumer_migration.md`.
**Pilot location:** branch `experiment/rust-numba-pilot`, dir `experiments/rust_kernels/`.

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

**Stage 2 — consumer wiring — in progress. RMSD family done (the proven pattern).**
Making `configure.kernel='rust'` take effect at the public API means routing the
*high-level analysis kernels* (the RMSD/geometry/axes/PCA/SASA/angle/dihedral/pbc leaves)
through the seam. It cannot be done by replacing kernel names at module level: several
primitives (`dot_product`, `get_distance_two_points`, the MIC and `math` helpers) are
called *inside* other `njit` kernels, and rebinding those to a Python dispatcher breaks
Numba compilation. So routing is at the high-level consumers, one family at a time, each
validated with its test group.

The **RMSD family** is wired and validated as the reference pattern: `get_rmsd`,
`get_least_rmsd`, `least_rmsd_fit` and the `_native_placers` build path now call the seam
(`from molsysmt._private import rust_backend as _kernels`) instead of `msmlib.structure.*`,
so they honour `configure.kernel` with no per-function argument. The 20 existing
RMSD/least-RMSD/fit tests pass on **both** the default Numba path and with
`configure.kernel='rust'`, and the two agree to the last bit end-to-end on a real
trajectory. `_private/gpu.py` (the GPU dispatch) is intentionally left for the GPU wiring —
Rust here is the CPU backend.

The **geometry family** (`get_center` incl. groups, `get_radius_of_gyration`, `get_rmsf`,
`flip`) is wired the same way; its 37 tests pass on both backends and agree to the last bit
end-to-end. Consumers importing the *public* `structure.get_center` (e.g. `center`,
`move_away`, `align_principal_axes`) inherit the routing for free.

All analysis families are now routed and validated on both backends (default Numba and
`configure.kernel='rust'` forced), each against its own test group:

| family | consumers routed | tests (numba / rust) |
|---|---|---|
| RMSD | get_rmsd, get_least_rmsd, least_rmsd_fit, _native_placers | 20 / 20 |
| geometry | get_center, get_radius_of_gyration, get_rmsf, flip | 37 / 37 |
| axes + PCA | get_principal_axes, principal_component_analysis | 2 / 2 |
| angles + dihedrals | get_angles, get_dihedral_angles, set/shift_dihedral_angles | 11 / 11 |
| pbc | box geometry + wrap/unwrap + PDB handler | 52 / 52 |
| topology/series | component index, occurrence_order (convert path) | 22 / 22 |
| distances/neighbours/contacts | get_distances, get_neighbors, get_contacts | 88 / 88 |
| SASA | get_sasa (cell-list variants) | 16 / 16 |

**Coverage is now complete for the CPU surface.** The brute-force `get_sasa`/`get_mic_sasa`
kernels and the two `minimum_distance_*` math kernels — the only ported-gap left after the
first stage-2 pass — are now ported (`get_mic_sasa` corrects the same `_is_orthogonal` typo
as its cell-list sibling) and their consumers (`physchem.get_sasa` brute-force path,
`build.build_peptide`) route through the seam. Validated on both backends: brute-force SASA
is byte-identical end-to-end, its 9 direct parity tests pass, the 16 SASA tests pass on
both paths, and the build_peptide suite passes identically (148/148) under Numba and forced
Rust.

**The one remaining exception, deliberate:** `_private/gpu.py` is the GPU dispatch,
orthogonal to the CPU numba/rust choice (`use_gpu` selects GPU; `kernel` selects the CPU
backend). GPU-from-Rust is its own decision — see
`rust_gpu_backend_options.md`.

With these, `configure.kernel='rust'` now exercises Rust across the whole analysis surface
in dogfooding, while the default stays Numba and byte-identical.

**Stage 3 — CI wheels — not started.** Multiplatform `cp311-abi3` wheel builds are
repository infrastructure and are the gate for flipping the default to `'auto'`/`'rust'`.

## 0. Where we are

All 97 CPU `njit` kernels in `molsysmt.lib` have a Rust port behind an opt-in seam
(`molsysmt/_private/rust_backend.py`, `backend='numba'|'rust'|'auto'`), with 69 Rust unit
tests and 166 Python parity tests. `molsysmt` never imports the crate; Numba is the
default; there is **zero 1.0 debt**. The remaining work is not porting — it is a decision
about whether and how to make Rust the implementation and retire Numba.

This document is the plan for that decision. It should be the first thing that moves toward
`main`; the mechanisms follow it, not the other way round.

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

- **Redesign levers C/D/E** (fused multi-observable passes, columnar/SoA SIMD layout,
  Niggli-reduced cell for the triclinic MIC). These are Rust-kernel algorithmic redesigns,
  and while Numba is the oracle every one of them pays the parity tax twice. Once Rust is
  the implementation, they become ordinary work behind the property tests. See
  `rust_kernel_redesign_beyond_faithful_ports.md`.

## 6. What this explicitly does not do

- It does not make the cut a 1.0 blocker. If wheels are not ready, ship `'auto'`; the
  no-debt property holds and the flip waits.
- It does not touch the public numerical contract silently: the tolerance-level change is
  announced and dogfooded, and the three deliberate divergences are documented bugs where
  Rust is the correction.
