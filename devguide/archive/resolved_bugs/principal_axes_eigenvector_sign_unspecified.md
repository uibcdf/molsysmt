# Contract gap: the sign of the principal axes is unspecified

**Status:** **RESOLVED by the Rust-only cut (archived 2026-07-28).**
**Severity when open:** contract — results were mathematically correct, but not reproducible
**Scope when open:** `molsysmt/lib/structure/get_principal_inertia_axes.py`,
`molsysmt/lib/structure/get_principal_geometric_axes.py`, and the public functions above
them

> ## Resolution
>
> The Rust port that replaced these kernels in Segment D **specifies the sign**: it
> makes the component of largest absolute value positive, so a returned axis is a
> function of the input alone and cannot flip with a LAPACK version, a thread count,
> or a backend. See `fix_sign` and the module documentation in `rust/src/axes.rs`.
>
> Guarded by the Rust unit test `the_sign_convention_is_deterministic`, alongside
> property tests that assert the defining eigenvalue equation and axis orthogonality
> independently of any sign convention.
>
> The part of this report framed as a *disagreement between the `rust` and `numba`
> backends* is moot: there is one backend. The durable part — that an eigenvector is
> defined only up to sign, and that a public contract must therefore pick one — is
> now satisfied rather than merely reported.
>
> Everything below is the original report, retained for provenance. It describes the
> deleted Numba implementation and does not describe current behaviour.

## The gap

An eigenvector is defined only up to sign: if `v` is a principal axis, so is `-v`. Both
kernels return `np.linalg.eigh(...)[1].transpose()` directly, so **which of the two a
caller receives is whatever LAPACK happened to produce**.

That is not a defect in the arithmetic — the axes are correct either way — but it means
the returned array is not a function of the input alone. In particular it can change
with:

- the LAPACK implementation (OpenBLAS, MKL, Accelerate, reference netlib) and its version,
- the number of threads, for some drivers,
- an unrelated numpy or scipy upgrade,
- and, concretely today, the choice of compute backend (see below).

Anything downstream that consumes the axis direction rather than the axis *line* — an
alignment, a projection sign, a stored reference orientation, a regression test pinned to
values — can flip without any change in the science.

## Why it surfaced now

The Rust port of these kernels uses `nalgebra` instead of LAPACK. Both produce correct
axes, but they disagree on sign for some inputs, so `backend='rust'` and `backend='numba'`
would visibly return different arrays for identical input — axes flipping when the
accelerator is switched on. There is no way to "fix" that in the port, because there is no
specified answer to match.

## What the Rust port does

It fixes the sign deterministically: **the component of largest absolute value is made
positive**, ties broken by lowest index. The axes are mathematically identical; the
difference is that the result is reproducible across backends, platforms and LAPACK
versions.

## Suggested fix

1. **Adopt the same convention upstream** and state it in the docstrings, so the two
   backends agree and the output becomes a function of the input. The convention itself is
   arbitrary — any documented rule works — but it should be the *same* rule on both sides.
2. **Add a regression test** asserting the convention, plus the properties that do not
   depend on it: eigenvalues ascending, axes orthonormal, and `M v = λ v`.
3. While there, consider whether the two kernels' opposite orderings are intentional and
   documented: for a rod, the smallest *inertia* eigenvalue is along the rod, while the
   smallest *geometric* eigenvalue is perpendicular to it. Both are correct and both are
   returned ascending, but a caller reaching for "the long axis" will pick the wrong row in
   one of the two.

## Note on the parity tests

`tests/rust/test_axes_parity.py` compares eigenvalues directly and eigenvectors only up to
sign (`|v_rust · v_numba| = 1`), then asserts the defining property independently. That is
the correct shape for a test of an object defined up to sign, and it is worth keeping even
after a convention is adopted.

Related: `linear_algebra_backend_for_rust_kernels.md` (why these kernels use `nalgebra`
rather than LAPACK at all).
