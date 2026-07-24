# Rust kernels — Numba replacement (all 97 CPU kernels ported)

**Status:** every CPU `njit` kernel in `molsysmt.lib` has a Rust port behind the opt-in
seam (97/97). 69 Rust unit tests and 166 Python parity tests pass. `molsysmt` still never
imports the crate; Numba remains the default. What is left is a decision, not more porting:
make Rust the default and drop Numba, or stop here (see
`devguide/pending_proposals/rusterization_pilot_conclusions_and_adoption.md`).

## Migration policy (agreed)

- **Faithful in algorithm + floating-point operations** → keeps the bit-for-bit parity
  gate against the Numba oracle, which is what makes the migration safe and reviewable.
- **…but faithful to the oracle, not to its defects.** Bit-parity is the gate *where the
  oracle is defined*. Where the port uncovers a genuine upstream bug, Rust implements the
  correct behaviour, a test pins the divergence, and the defect is filed in
  `devguide/pending_bugs/`. Three cases so far, all reported:
  `sasa_is_orthogonal_typo.md` (well-defined but wrong branch — parity drops to a 1e-9
  tolerance, divergence measured at 4.4e-16),
  `dihedral_angles_broadcast_mismatch_pbc.md` (undefined: an unchecked out-of-bounds read,
  so there is no value to be faithful to) and
  `wrap_to_mic_triclinic_not_minimum_image.md` (plainly wrong results — the parity
  assertion is replaced by a property assertion). Copying a bug forward would fossilise it
  behind a green test suite. Each such test also fails if upstream is fixed, so a
  divergence cannot outlive its justification.
- **Bit-parity has a floor, and it is `fastmath`.** `lazy_njit` compiles with
  `fastmath=True`, so LLVM may contract or reassociate; Rust does not by default. Where
  that bites (the `pbc` triclinic wraps) the gate is a 1e-12 tolerance, confirmed by
  rebuilding the oracle with `fastmath=False` and recovering exact parity.
- **Free in structure and parallelism** ("level A"): stack arrays instead of per-element
  `np.empty`, `Vec` instead of pre-sized numpy scratch, and `rayon` where the Numba
  kernel used `prange`. These do not change results — and they are where the big wins
  came from (the MIC port's 14–27× warm).
- **Parity-breaking optimisation is a separate, later phase** ("level B": float
  reordering/SIMD; "level C": algorithmic or layout redesign, i.e. the columnar-engine
  work). Those change the gate from bit-parity to scientific tolerance and get their own
  benchmark. Never mixed with a port.

## Testing: two independent layers

1. **Rust unit tests** (`cargo test --no-default-features`, 69 tests) — exercise the
   pure helpers directly and cover edge cases the parity tests share blind spots on:
   inverse round-trips, minimum-image wrapping picking the short image, `angle`
   clamping so `acos` never NaNs, sorted/unsorted emit order, empty neighbour sets, and
   cumulative CSR offsets, the deliberate corrections above, and the
   round-half-to-even trap in `unwrap`. `extension-module`
   is an optional (default-on) feature precisely so the test binary can link.
2. **Python parity tests** (`tests/rust/`, 166 tests + 3 documented skips) — bit-for-bit equivalence against
   the Numba oracle through the opt-in seam — with the documented exceptions above (the
   SASA MIC path at 1e-9, the `pbc` triclinic wraps at 1e-12, and three skips where
   upstream is wrong) — skipped entirely when the wheel is absent. Run with `python -m pytest --receptor=llm
   tests/rust/`.

## Block 13: PCA (`pca.rs`) — the last CPU kernel, 97/97

`principal_component_analysis`, the one kernel `linear_algebra_backend_for_rust_kernels.md`
left open. Two deliberate departures from a faithful port, both recommended there:

1. **The covariance is a matrix product, not the triple loop.** Upstream's
   `O(n_structures · n_features²)` scalar loop is exactly `Xc^T Xc`; building it as a
   `faer` rank-k update is the redesign the proposal called the archetype of "trapped in
   the translation". This is the one kernel where a faithful port would have preserved a
   mis-transcribed matrix multiply.
2. **`faer`, not `nalgebra`.** The matrix is `3N × 3N` (2400×2400 for 800 atoms) — dense
   and large, `faer`'s domain, not the fixed-size 3x3/4x4 that `nalgebra` handles for the
   other blocks. Still pure Rust: no BLAS system dependency, the abi3 wheel survives.

**Performance** (this machine, warm; faer running parallel on all cores):

| n_atoms | n_features | n_structures | rank | numba | rust | speedup |
|---|---|---|---|---|---|---|
| 200 | 600 | 500 | 500 | 0.23 s | 0.15 s | 1.5x |
| 500 | 1500 | 500 | 500 | 1.24 s | 0.38 s | 3.2x |
| 800 | 2400 | 300 | 300 | 2.41 s | 1.02 s | 2.4x |
| 800 | 2400 | 1000 | 1000 | 6.29 s | 1.14 s | **5.5x** |

1.5–5.5x, and the spread is informative. The covariance build is `O(n_structures · n_f²)`,
so its cost — and the win from doing it as a matmul — grows with the number of structures:
the 5.5x is a 1000-structure trajectory, the regime that actually matters. The
eigendecomposition is the residual cost, and there faer is competitive rather than
dominant: on a full-rank 2400×2400 symmetric matrix, numpy's **MKL** (multi-threaded) does
`eigh` in 0.70 s against faer's 1.27 s parallel / 4.12 s sequential — roughly 1.8x behind
Intel's hand-tuned LAPACK, and closer against a pip/OpenBLAS numpy. "Pure-Rust and within
~2x of MKL" is what *competitive* means; it is not "much slower", and an earlier draft of
this note overstated it.

Two lessons worth keeping:

- **faer's high-level `self_adjoint_eigen` defaults to sequential.** The kernel must set
  `faer::set_global_parallelism` (and release the GIL) or it silently runs single-threaded
  — a ~3x self-inflicted slowdown at n=2400 that was in the first version of this port.
- **Parallelism is not the kernel's decision to make.** `Par::rayon(0)` (all cores) is
  hardcoded for the pilot only. Integration must drive it from `molsysmt.configure`
  (`parallel_mode`, `num_threads`) — the same global mechanism the Numba kernels already
  honour, with a uniform per-call `parallel=`/`num_threads=` override — not from inside the
  kernel and not via a new PCA argument.

Parity is at tolerance, and the eigenvectors need the most care in the whole migration:
a **sign** ambiguity (fixed deterministically, largest-magnitude component positive) *and*
a **degeneracy** problem — when `n_structures < n_features` the covariance is rank
deficient and its null space has an arbitrary eigenvector basis. The parity test compares
eigenvalues within tolerance, eigenvectors up to sign only where the eigenvalue is nonzero
and well separated, and otherwise asserts `cov v = λ v`. See
`devguide/pending_bugs/principal_axes_eigenvector_sign_unspecified.md`.

## Blocks 11 and 12: the RMSD family and the principal axes (`rmsd.rs`, `axes.rs`)

The kernels that were blocked on the linear-algebra decision, resolved by
`devguide/pending_proposals/linear_algebra_backend_for_rust_kernels.md`: **`nalgebra`, in
pure Rust, no BLAS system dependency.** The matrices are 4x4 (the quaternion/Kearsley `F`
of the RMSD superposition) and 3x3 (the inertia and second-moment tensors), so LAPACK
would buy nothing and would cost the self-contained abi3 wheel.

`rmsd.rs` ports `get_rmsd` (a plain reduction, no superposition), `get_least_rmsd` (needs
only the largest eigenvalue) and `get_least_rmsd_rotation_and_translation` (needs the
matching eigenvector, used as a rotation quaternion) — 9 kernels.
`axes.rs` ports the four principal-axis kernels.

**Parity is at tolerance here for reasons that cannot be engineered away**: `fastmath`, a
different eigensolver from LAPACK's `dsyevx`, and upstream's `np.sum` for the centroid,
which sums pairwise rather than sequentially. All last-bit effects.

### Sign ambiguity: it cancels in one block and not in the other

- **RMSD**: `q` and `-q` give the same rotation matrix, so the kernel output is well
  defined even though the quaternion is not. An ordinary tolerance comparison is valid.
- **Principal axes**: the eigenvectors are returned raw, so upstream's output is whatever
  LAPACK produced and is not a function of the input alone. The port fixes signs
  deterministically (largest-magnitude component positive) so switching backend cannot
  flip an axis, and the parity test compares eigenvectors *up to sign*
  (`|v_rust · v_numba| = 1`) while asserting `M v = λ v` independently. Reported as
  `devguide/pending_bugs/principal_axes_eigenvector_sign_unspecified.md`.

Both blocks lean on property tests rather than parity alone: that the returned transform
actually superposes the structures, that the rotation is proper (orthogonal, determinant
+1, not a reflection), that a rod's smallest inertia axis lies along the rod. Those would
catch a convention error both backends happened to share, which no parity assertion can.

## Block 10: the mechanical long tail (`geometry.rs`, `series.rs`, `topology.rs`)

Ports the 17 remaining kernels that need no linear algebra: `get_center` (4 variants),
`flip`, `get_radius_of_gyration`, `get_rmsf`, all of `lib/series.py`, and the union-find
behind `get_component_index_from_bonded_atom_pairs`. Parity test:
`tests/rust/test_long_tail_parity.py`.

**The timings are the most useful part, because two of them are ties** (50 structures x
4000 atoms):

| kernel | COLD nb | COLD rs | WARM nb | WARM rs | warm |
|---|---|---|---|---|---|
| `flip` | 603.5 ms | 3.4 ms | 22.5 ms | 0.9 ms | **25.3x** |
| `get_center` | 630.8 ms | 2.0 ms | 0.6 ms | 0.1 ms | **5.1x** |
| `get_radius_of_gyration` | 604.6 ms | 0.8 ms | 0.5 ms | 0.6 ms | 0.9x |
| `get_rmsf` | 596.1 ms | 1.1 ms | 0.7 ms | 0.8 ms | 0.9x |

`flip` builds two numpy temporaries per atom; `get_center` accumulates into a `np.zeros(3)`
per atom. `get_radius_of_gyration` and `get_rmsf` are already written as scalar loops
upstream — nothing to reclaim, and Rust is marginally *slower*. This is the clearest
statement of the rule the whole migration has been converging on: **Rust buys cold-start
and allocation, not arithmetic.** Where Numba is already allocation-free, warm performance
is a coin flip, and the honest reason to port those kernels is uniformity and dropping the
JIT dependency, not speed.

### Parity splits by data type

Integer kernels (series, topology) are bit-for-bit — there is no rounding to disagree
about. The floating-point reductions need a 1e-12 tolerance for the same `fastmath` reason
as block 9, now reaching plain accumulation loops rather than just dot products: LLVM may
vectorise a long sum into partial sums. Verified the same way — Numba fastmath-vs-no-fastmath
differs on exactly the same 10/21 centre components that Rust does, and Rust matches a
`fastmath=False` build on 0/21.

Two `series` kernels index `serie[0]` before checking the length, so an empty input is an
unchecked out-of-bounds read; the ports return empty output and a test pins the divergence
(failing if upstream is ever fixed). `_jit_serialize` takes a Numba typed list of typed
lists upstream and a plain Python sequence here, so the seam converts only on the Numba
path — and an empty segment needs an explicit `nb.typed.List.empty_list(nb.int64)`, since
Numba cannot infer the item type of an empty list.

## Block 9: the `pbc` package (`pbc.rs`)

Ports all of `molsysmt.lib.pbc` — `box_is_orthogonal`, `get_lengths_from_box`,
`get_angles_from_box`, `get_lengths_and_angles_from_box`, `get_box_from_lengths_and_angles`,
`wrap_to_pbc`, `wrap_to_pbc_center`, `wrap_to_mic` and `unwrap` (17 exported functions).
Parity test: `tests/rust/test_pbc_parity.py`.

**No rayon anywhere in this block** — the upstream kernels use plain `range`, and `unwrap`
carries a loop dependency (structure *s+1* is written from the already-updated *s*), so it
is serial by construction. That makes the timings a like-for-like single-threaded
comparison, and the win is purely the removal of per-atom allocation: upstream allocates
~4 numpy arrays per atom in `wrap_to_pbc`, and ~81 per atom in the triclinic `wrap_to_mic`
(the 27-image search allocates three vectors per candidate).

| kernel | box | COLD nb | COLD rs | WARM nb | WARM rs | warm speedup |
|---|---|---|---|---|---|---|
| `wrap_to_pbc` | orthogonal | 554.9 ms | 4.6 ms | 20.8 ms | 2.9 ms | **7.2x** |
| `wrap_to_pbc` | triclinic | 554.0 ms | 4.8 ms | 27.4 ms | 2.7 ms | **10.0x** |
| `wrap_to_mic` | triclinic | 863.2 ms | 12.4 ms | 305.8 ms | 10.7 ms | **28.7x** |

(20 structures x 5000 atoms.) This is the cleanest confirmation so far of the pattern the
earlier blocks suggested: **the warm win tracks allocation volume, not parallelism.**

### Three parity regimes, and one of them is about the oracle itself

- **Orthogonal boxes: bit-for-bit.**
- **Triclinic boxes: 1e-12 tolerance, and Numba is the reason.** `lazy_njit` sets
  `fastmath=True`, letting LLVM contract the fractional wrap's three-term dot products
  into FMAs; Rust does not fuse by default. 738/2000 sampled vectors differ, max 6.2e-15.
  This was *verified* rather than assumed: recompiling the same kernel with
  `fastmath=False` makes Numba and Rust agree on **2000/2000**, and the no-fastmath
  divergence count against the fastmath build is also exactly 738/2000. Nothing on the
  Rust side can close this without guessing LLVM's contraction choices, which would be
  brittle and compiler-version-dependent.

  This is a general constraint on the migration, not a fact about `pbc`: bit-for-bit
  parity is attainable only where fastmath happens to be a no-op. Earlier blocks got it
  because their arithmetic was not reassociated, not because the gate is absolute.
- **`wrap_to_mic` on triclinic boxes: deliberately corrected, no parity assertion.**
  Upstream applies the minimum image convention on orthogonal boxes but not on triclinic
  ones (minimum image in only 55/300 sampled vectors) because its 27-image search iterates
  images of the *original* vector rather than the wrapped one — so when the input is
  several box lengths out, the corner-cell wrap wins by default. Searching around the
  wrapped candidate gives 300/300, and it is what `unwrap.py` in the same package already
  does. Filed as `devguide/pending_bugs/wrap_to_mic_triclinic_not_minimum_image.md`; the
  test asserts the property and **fails loudly if upstream is ever fixed**, so the
  divergence cannot outlive its reason.

`unwrap` also pins a rounding trap: Python and Numba `round` half **to even** (verified:
0.5 -> 0, 2.5 -> 2), while `f64::round` rounds half away from zero. The port uses
`round_ties_even`; a unit test asserts both, because getting it wrong displaces an atom by
a full box length on exact ties.

## Block 7: shared math helpers (`mathlib.rs`)

Ports `molsysmt.lib.math` — the single largest `njit` file (13 sites) — and, just as
importantly, **pays off duplication the earlier blocks had accumulated**: `cross`,
`dot`, `norm`, `angle`, `dihedral_angle` and the 3x3 inverses had each been
re-implemented locally in `mic.rs`, `neighbors.rs`, `sasa.rs`, `angles.rs` and
`dihedrals.rs`. They now live in one place and every module imports them.

Two 3x3 inverses are deliberately kept separate and a unit test pins the difference:
`inverse_matrix_3x3` is `math.py`'s (valid only for the lower-triangular box
convention) while `inverse_matrix_3x3_full` is the general Cramer inverse inlined by
`neighbor_list`/`get_sasa`. They agree on lower-triangular boxes and diverge on general
matrices — swapping them would silently change results.

`rodrigues_rotation` and `quaternion_to_rotation_matrix` are ported here because they
unlock later blocks (the set/shift dihedral kernels and the RMSD superposition family).
Note the Numba `rodrigues_rotation` mutates its argument in place and returns `None`;
the Rust one returns the rotated vector and the seam normalises both.

**Another unit test earned its keep**: the first version asserted the two inverses were
never equal, which is wrong — they agree precisely on the lower-triangular convention.
Parity was green throughout; only the native test caught the bad premise (mine again).

## Block 6: dihedral-angle family

`src/dihedrals.rs` ports `get_dihedral_angles{,_single_structure}` and
`get_mic_dihedral_angles{,_single_structure}`, reusing the MIC helpers. Heaviest
per-element allocation of the geometry kernels: the Numba versions build three numpy
vectors per quartet and `dihedral_angle` calls `cross_product` three times, each with
`np.empty((3))` — six allocations per quartet, nine in the MIC variants. The sign
convention (negated when `cross(aux0,aux1)·vect1 <= 0`) is part of the contract, so the
parity test compares signed values.

**A unit test earned its keep here.** The first version of the planar-conformation test
asserted the wrong geometry (I had cis and trans swapped). The Python parity tests were
green — because the port *does* match Numba — so only the native unit test caught the
mistake, which was mine and not the kernel's. The corrected expectations were
cross-checked against the Numba oracle (`v2=[1,-1,0] → 0`, `v2=[1,1,0] → -pi`,
`v2=[1,0,±1] → ∓pi/2`).

## Block 5: (non-periodic) distance family

`src/distances.rs` ports the six `molsysmt.lib.structure.get_distances.*` functions —
the vacuum counterpart of block 1, and the most-used fallback (the full distance matrix
behind `get_neighbors`/`get_contacts` when the cell list does not apply). Chosen because
the Numba helper `get_distance_two_points_single_structure` does
`tmp_vect = point2 - point1`, i.e. **one numpy allocation per pair → O(N²) allocations**,
the heaviest allocation volume of the remaining candidates. rayon over structures for
the matrix-producing variants (each structure writes a disjoint slab, so results are
unchanged). Parity test: `tests/rust/test_distances_parity.py` (also asserts the
self-matrix is symmetric with a zero diagonal).

## Block 4: angle family

`src/angles.rs` ports `get_angles{,_single_structure}` and
`get_mic_angles{,_single_structure}`, reusing the MIC helpers from `mic.rs`. Chosen
because the Numba versions allocate **four arrays per triplet** (two numpy subtractions
plus two `np.empty((3))` inside `wrap_to_mic_vector`) — the pattern that produced the
14–27× warm win in block 1 — and because `get_angles` is on the
`hbonds.get_luzard_chandler_hbonds` path, completing the h-bond chain started in block 2.
Parity test: `tests/rust/test_angles_parity.py`.

## Block 3: cell-list Shrake–Rupley SASA

`src/sasa.rs` ports `get_sasa_cell_list` / `get_mic_sasa_cell_list` (per-structure grid
— bounding box for vacuum, fractional/periodic for MIC — candidate gather, sphere-point
occlusion). rayon over the flattened (structure, atom) work with per-thread scratch.
Parity test: `tests/rust/test_sasa_cell_list_parity.py` (vacuum + orthogonal/triclinic,
one vs many structures, plus zero-radius dummy atoms).

**Corrected upstream typo:** `get_sasa.py::_is_orthogonal` tests `box_s[2,2]` where it
means `box_s[2,1]`. `box_s[2,2]` is a box length, so the check is always false and the MIC
path *always* takes the triclinic branch, even for cubic boxes. This port uses the intended
check; upstream correctness is unaffected (the triclinic wrap is general), so the upstream
cost is performance only.

Measured consequence: the two branches are mathematically identical but not bit-identical
(one divides, the other multiplies by a Cramer reciprocal) — 11094/20000 wrap probes
differ at max 1.78e-15, propagating to **max 4.4e-16 in SASA values (relative 4.4e-16)**
with no occlusion decision flipping. So this kernel's parity test runs at 1e-9 tolerance
rather than bit-equality on orthogonal boxes. Filed as
`devguide/pending_bugs/sasa_is_orthogonal_typo.md`.

| case | COLD nb | COLD rs | WARM nb `auto` | WARM nb forced-par | WARM rust |
|---|---|---|---|---|---|
| 1 struct × 4000 | 385.0 ms | 8.0 ms | 51.1 ms | **7.1 ms** | 9.0 ms |
| 20 struct × 1500 | 222.9 ms | 43.2 ms | 216.6 ms | **27.6 ms** | 28.4 ms |

Third independent confirmation of the same pattern: **like-for-like warm is a tie**
(Numba 21% ahead in the first case, ~3% in the second), while cold (48× / 5×) and the
default-configuration gating (5.7× / 7.6×) are where Rust wins.

## Block 2: multi-structure CSR neighbour list

`src/neighbors.rs` ports `molsysmt.lib.structure.neighbor_list.neighbor_list_csr_multi`
(the hot kernel behind `get_contacts` and `get_neighbors`): per-structure linked-cell
grid, vacuum + periodic (orthogonal/triclinic, neighbor_list's MIC convention — full
inverse, nearest-image round, no 27-image search), global flat CSR, optional sort by
distance. Parallelised with `rayon` over the flattened (structure, query-atom) work with
the GIL released; the CSR is assembled in work order, so the result is unchanged.
Parity test: `tests/rust/test_neighbor_list_parity.py` (vacuum/PBC × self/disjoint ×
sorted/unsorted, comparing offsets+indices+distances exactly). Adding rayon was verified
**after** landing the serial port, and parity stayed exact — demonstrating the policy.

### Benchmark — and an honest reading (`bench_neighbors.py`)

After the level-A fix (per-thread scratch buffers via rayon `map_init`, so the gather
loop stops reallocating — parity unchanged, 21 tests still green):

| case | numba `auto` (default) | numba **forced parallel** | rust (rayon + scratch) |
|---|---|---|---|
| 1 struct × 8000 | 91.4 ms | **10.8 ms** | 11.9 ms |
| 50 struct × 2000 | 395.9 ms | **39.8 ms** | 43.7 ms |

Cold (first call): numba 678 / 376 ms vs rust 12.5 / 54.7 ms.
The scratch fix took the allocation-heavy case from 53.1 → 43.7 ms (−18%); the other case
was unchanged (noise).

**Honest reading — like-for-like (both parallel) this is a tie, with Numba marginally
ahead (~10%)**, and run-to-run variation is ~20%, so that gap is within noise. Rust does
**not** win on warm throughput here; well-written Numba is already at C speed.

The large apparent win is a *default-configuration* effect: with `parallel_mode='auto'`
and `parallel_threshold=500000`, these payloads (24k and 300k elements) fall below the
gate, so **Numba runs serial** (91 / 396 ms) while rayon always parallelises (12 / 44 ms).
That is a genuine user-facing advantage — the gate exists partly because of the
Numba-parallel segfault class, which Rust does not have — but the mechanism is the gating,
not raw Rust speed.

This reinforces the overall conclusion: Rust's value is cold start, robustness and the
absence of gating, plus the allocation-heavy production kernels (the MIC family's 14–27×),
not warm throughput on already-tight numeric loops.

## First migrated block: MIC distance family

`src/mic.rs` ports the full `molsysmt.lib.structure.get_mic_distances.*` family
(6 functions: single/two-system, all-pairs/pairs, multi- and single-structure;
orthogonal + triclinic 27-image MIC) with names matching Numba 1:1. Opt-in seam:
`molsysmt/_private/rust_backend.py` (`backend='numba'|'rust'|'auto'`, Numba default and
oracle). Parity test: `tests/rust/test_mic_distances_parity.py` (bit-for-bit, skipped
unless the wheel is installed). This is the template each subsequent block follows:
*port faithfully → dispatch via the seam → parity test in the suite*, with Numba
staying the default so 1.0 depends on none of it.

---


Isolated experiment on the `experiment/rust-numba-pilot` branch. It reimplements a
couple of MolSysMT numeric kernels in Rust (PyO3 + rust-numpy) to measure numerical
parity and warm/cold timing against the Python/Numba versions.

**This is self-contained and disposable.**
- It is NOT referenced by molsysmt's build; molsysmt builds and imports exactly the
  same with or without this crate.
- molsysmt never imports `msm_rust_kernels`. Any future use would be opt-in behind a
  `try: import msm_rust_kernels except ImportError:` fallback to Numba.
- To drop it: abandon the branch / `git worktree remove`. Nothing else changes.

## Build & run

Toolchain: `rust` + `maturin` (installed via conda-forge into the active env).

```bash
cd experiments/rust_kernels
maturin develop --release      # builds and installs msm_rust_kernels into the env
python bench_parity.py         # parity + warm/cold timing vs Numba
```

## Results — benchmark matrix (one machine, 20 threads)

`bench_matrix.py` covers four computational profiles. **Parity is exact (bit-for-bit)
in every case.** Warm = best of N; cold = first call (Numba pays JIT).

| profile | kernel | WARM numba | WARM rust | verdict (warm) |
|---|---|---|---|---|
| regular arithmetic O(N²) | pairwise sqdist (N=4000) | 85.9 ms | 85.6 ms | tie |
| transcendental O(N²) | coulomb sqrt/÷ (N=4000) | 64.4 ms | 65.5 ms | tie |
| branchy / irregular ~O(N) | neighbour counts (N=20000) | 101.8 ms | 88.1 ms | rust ~15% faster |

**Cold path (the decisive axis), per kernel:**

| kernel | COLD numba (JIT) | COLD rust (AOT) |
|---|---|---|
| pairwise (N=500) | 484 ms | 1.6 ms |
| coulomb (N=500) | 238 ms | 1.2 ms |
| neighbour counts (N=5000) | 1327 ms | 5.0 ms |
| **aggregate across kernels** | **2048 ms** | **7.7 ms** (~266×) |

**Parallel (Coulomb N=4000, 20 threads):** serial numba 68 ms / rust 66 ms (tie);
parallel numba 12.4 ms (5.5×) / rust 10.3 ms (6.4×). Rust's rayon scales slightly
better and needs no `parallel_mode`/`parallel_threshold` gating.

## Item 1 — a REAL production kernel (`get_mic_distances_single_system`)

`bench_production.py` ports the actual MIC all-pairs distance kernel (orthogonal +
triclinic 27-image refinement) and runs it on real MolSysMT coordinates (N=1488).

| box | parity | COLD numba | COLD rust | WARM numba | WARM rust |
|---|---|---|---|---|---|
| orthogonal | exact (0.0) | 721 ms | 26 ms | 248 ms | 17 ms (**14×**) |
| triclinic | exact (0.0) | 3367 ms | 131 ms | 3324 ms | 122 ms (**27×**) |

**This revises the synthetic "warm is a tie" finding.** On a real kernel Rust is
14–27× faster *warm* too — because the production code is written naturally
(`np.empty((3))` per pair, nested njit calls `wrap_to_mic`→`norm`, array slicing) and
Numba does not eliminate that allocation/call overhead, whereas the Rust port uses
stack arrays (`[f64;3]`, zero heap). Caveat: a hand-optimised Numba (pre-allocated
scratch, inlined) would narrow the warm gap — so part of this is "Rust vs naturally
written Numba", not "Rust vs optimal Numba". The point is that Rust delivers optimal
performance from readable code, for free.

## Conclusions

1. **Numerically safe** — exact parity across regular, transcendental and branchy
   kernels.
2. **Warm throughput is a tie** — well-written Numba is already at C speed; Rust does
   not make steady-state math meaningfully faster (it edges ahead only on
   branchy/irregular code — graphs, cell lists, selections).
3. **Cold/warmup is where Rust wins, and it compounds** — ~266× aggregate; a single
   complex kernel costs >1 s to JIT, and the repo has ~107 njit sites. This is the
   real payoff: no `warmup()`, instant start, and no JIT-parallel failure class.
4. **Parallelism ≥ Numba** with rayon, without the config gating or segfault risk.

**Verdict:** Rust is not a "faster math" play (warm is a tie) — it's an
instant-start / robust / parallel-safe play, with a bonus edge on the irregular
graph/spatial algorithms that are exactly the columnar-engine direction.

_Caveats: hand-written kernels (not the production ones), no SIMD tuning on either
side, single machine._
