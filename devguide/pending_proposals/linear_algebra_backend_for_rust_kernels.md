# Linear-algebra backend for the Rust kernels

**Status:** **accepted and fully implemented** (2026-07-24). The 10 small-matrix
kernels use `nalgebra`; PCA (section 6.2) is ported with `faer` per the second option, so
all 97 CPU kernels are now in Rust. Measured PCA speedup is 1.5-5.5x (growing with the
number of structures, since the covariance cost is `O(n_structures · n_f²)`): the covariance
rewrite dominates the win, and faer's dense eigensolver is competitive on the residual —
~1.8x behind multi-threaded MKL on a 2400×2400 matrix, closer against OpenBLAS. Note faer's
high-level eigensolver defaults to sequential and must be told to parallelise, and that
parallelism must be driven from `molsysmt.configure`, not a per-function argument.
**Relates to:** `rusterization_pilot_conclusions_and_adoption.md`,
`rusterization_heavy_computations.md`,
`trajectory_projection_onto_principal_components.md`.
**Pilot location:** branch `experiment/rust-numba-pilot`, dir `experiments/rust_kernels/`.

## 1. The question

The Rust migration has ported 83 of the 97 CPU `njit` kernels. Every one of the 11
remaining kernels that is actually blocked calls `np.linalg.eigh` or `eigvalsh`. Hence:
**is there a LAPACK/MKL-class solution for Rust, and should we take it?**

(Note that `get_rmsd.py`'s 3 kernels were previously counted as blocked; they are plain
RMSD without superposition and need no linear algebra at all. The blocked set is 11.)

## 2. The landscape

Yes, at two levels.

**LAPACK/BLAS linked from Rust**

| crate | what it gives |
|---|---|
| `ndarray-linalg` | `eigh`, `eigvalsh`, `svd` over `ndarray`; backend chosen by feature: `openblas-static`, `openblas-system`, `netlib`, **`intel-mkl`** |
| `lax` | the low-level LAPACK binding underneath it (`dsyevd`/`dsyevr` directly) |
| `blas-src`, `lapack-src`, `openblas-src`, `intel-mkl-src` | backend resolution and linking |

**Pure Rust, no LAPACK**

| crate | what it gives |
|---|---|
| `faer` | dense linear algebra with performance competitive with OpenBLAS/MKL; self-adjoint (symmetric) eigendecomposition, SVD, Cholesky |
| `nalgebra` | `SymmetricEigen` and friends; designed for small and fixed-size matrices |

The registry resolves all of these from the pilot crate; availability is not the
constraint.

## 3. What the kernels actually need

Availability is not the question — **size** is. The blocked kernels are not one problem
but two, and they have different answers:

| kernels | matrix | count |
|---|---|---|
| `get_least_rmsd`, `get_least_rmsd_rotation_and_translation` | **4x4 symmetric** | 6 |
| `get_principal_inertia_axes`, `get_principal_geometric_axes` | **3x3 symmetric** | 4 |
| `principal_component_analysis` | 3N x 3N dense symmetric | 1 |

The RMSD family uses the quaternion (Horn/Kearsley) method: it builds a 4x4 matrix `F`
from the correlation matrix and takes the eigenvector of its largest eigenvalue as a
rotation quaternion. For 3x3 and 4x4 symmetric matrices, LAPACK is the wrong tool — a
cyclic Jacobi sweep is some 40 lines and converges to machine precision in a handful of
iterations, and `nalgebra` provides it off the shelf at no packaging cost.

**So 10 of the 11 blocked kernels do not need LAPACK at all.** Only PCA is a genuinely
large dense problem.

## 4. Measurement: where PCA actually spends its time

The natural assumption is that the 3N x 3N eigendecomposition dominates PCA and is
therefore the thing needing a fast backend. Measured, that is false.

`principal_component_analysis` builds the covariance with a scalar triple loop,
`O(n_structures · n_features² / 2)`, and only then calls `eigh`. Timings (this machine,
`eigh` measured separately on a matrix of the same size; the covariance share is the
remainder):

| n_atoms | n_structures | n_features | Numba total | `eigh` alone | covariance | covariance via BLAS | speedup available |
|---|---|---|---|---|---|---|---|
| 200 | 500 | 600 | 0.30 s | 0.02 s | 0.27 s | 0.00 s | **132x** |
| 500 | 500 | 1500 | 1.32 s | 0.16 s | 1.16 s | 0.01 s | **96x** |
| 800 | 300 | 2400 | 2.49 s | 0.60 s | 1.89 s | 0.04 s | **48x** |

The eigendecomposition is **7-24% of the total**. The covariance build is the rest, and
`X.T @ X` — a rank-k update, BLAS `dsyrk` — does the identical work 48-132x faster.

The two costs scale differently (covariance `∝ n_structures · n_f²`, eigh `∝ n_f³`), so
the eigh share grows with system size; extrapolating the measured ratios they become
comparable somewhere around 1500-2000 atoms at a few hundred structures. Even there,
the covariance remains at least half the bill.

**Consequence:** for PCA the valuable backend property is fast BLAS-level matrix
multiplication, not a fast eigensolver.

**Consequence worth stating separately:** the single largest win available in this kernel
does not require Rust. Rewriting the covariance build as a numpy `X.T @ X` gets 48-132x
today, with no new dependency and no Rust at all. That should be evaluated on its own
merits regardless of what this proposal decides.

## 5. The deciding constraint: packaging

The adoption plan rests on a single self-contained `cp311-abi3` wheel with no runtime
dependencies. Linking LAPACK breaks that:

- `openblas-static` — builds OpenBLAS from source in CI, needs a Fortran toolchain, and
  inflates the wheel substantially.
- `openblas-system` / `intel-mkl` — a runtime system dependency; "pip install and it
  works" no longer holds.
- MKL is x86-only, so ARM and Apple Silicon are lost, and it carries redistribution terms
  that a scientific library should not casually inherit.

`faer` delivers LAPACK-class dense performance with none of those three consequences.

The historical objection to a third-party backend — that it would break bit-for-bit
parity with the Numba oracle — **no longer applies**. Blocks 9 and 10 established that
`lazy_njit`'s `fastmath=True` already puts a ~1e-15 floor under parity wherever a kernel
contains a reduction, verified by rebuilding the oracle with `fastmath=False` and
recovering exact agreement. These kernels will be gated at scientific tolerance whatever
backend we choose.

## 6. Recommendation

1. **3x3 and 4x4 (10 kernels): `nalgebra`, or a hand-written Jacobi sweep.** Pure Rust,
   no packaging cost, and the natural fit for fixed small matrices.
2. **PCA (1 kernel): do not port it to chase the eigensolver.** Either rewrite the
   covariance build in numpy (largest win, zero cost, no Rust), or, if the goal of
   removing Numba entirely takes precedence, use `faer` for both the rank-k update and
   the eigendecomposition.
3. **Do not take a BLAS/LAPACK system dependency.** The single-wheel property is worth
   more than the remaining margin over `faer`.

## 7. Note for whoever writes the parity tests

Eigenvectors carry a **sign and ordering ambiguity**, so these kernels cannot be compared
against Numba element-by-element even with a tolerance. Two observations:

- For the **RMSD family the ambiguity cancels**: `q` and `-q` produce the same rotation
  matrix, so the kernel output is well defined and an ordinary tolerance comparison is
  valid.
- For the **principal axes it does not**: the eigenvectors are returned directly.
  Compare the spanned subspace, or fix signs with an explicit stated convention, and
  assert the defining property (`M v = λ v`, orthonormality) rather than the raw array.

This is where an error would most plausibly hide, and it is test design, not kernel
design.
