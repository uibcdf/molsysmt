"""Parity of the Rust PCA kernel against the Numba oracle.

PCA is the hardest kernel to compare, for reasons stacked on top of each other:

* eigenvalues carry the usual `fastmath` + different-eigensolver tolerance;
* eigenvectors carry a **sign** ambiguity (`v` vs `-v`), fixed deterministically in the
  port but present in Numba's raw LAPACK output;
* and, uniquely, a **degeneracy** problem: when ``n_structures < n_features`` the
  covariance is rank deficient, so a whole null space shares eigenvalue 0 and its
  eigenvectors are an arbitrary orthonormal basis -- not comparable even up to sign.

So the tests compare eigenvalues within tolerance, compare eigenvectors up to sign *only*
where the eigenvalue is nonzero and well separated from its neighbours, and otherwise fall
back to the defining property ``cov v = lambda v``, which no ambiguity can touch. The
full-rank case (``n_structures >> n_features``) is exercised separately so there is at
least one regime where every eigenvector is individually comparable.
"""

import numpy as np
import pytest

import molsysmt._rust  # noqa: F401, E402

from molsysmt._private import rust_backend as rb  # noqa: E402

TOL = 1e-8


def _system(n_structures, n_atoms, seed=2026):
    rng = np.random.default_rng(seed)
    c = np.ascontiguousarray(rng.uniform(-8.0, 8.0, size=(n_structures, n_atoms, 3)))
    w = np.ascontiguousarray(rng.uniform(1.0, 16.0, size=n_atoms))
    return c, w


def _covariance(c, w):
    """Rebuild the covariance independently, to test the eigen-equation without a backend."""
    ns, na = c.shape[0], c.shape[1]
    nf = na * 3
    flat = np.empty((ns, nf))
    for xx in range(nf):
        ii, jj = xx % na, xx // na
        flat[:, xx] = c[:, ii, jj]
    mean = flat.mean(axis=0)
    wpf = np.sqrt(w[np.arange(nf) % na])
    xc = (flat - mean) * wpf
    return (xc.T @ xc) / ns


def test_eigenvalues_match_the_oracle():
    c, w = _system(400, 40)  # full rank: n_structures >> n_features (120)
    nb_val, _ = rb.principal_component_analysis(c, w, backend="numba")
    rs_val, _ = rb.principal_component_analysis(c, w, backend="rust")
    assert nb_val.shape == rs_val.shape == (120,)
    assert np.allclose(nb_val, rs_val, rtol=TOL, atol=TOL), "eigenvalues diverged"
    assert np.all(np.diff(rs_val) >= -1e-9), "eigenvalues must be ascending"


def test_eigenvectors_match_up_to_sign_when_full_rank():
    c, w = _system(
        500, 30
    )  # 90 features, full rank -> generically distinct eigenvalues
    nb_val, nb_vec = rb.principal_component_analysis(c, w, backend="numba")
    rs_val, rs_vec = rb.principal_component_analysis(c, w, backend="rust")
    assert np.allclose(nb_val, rs_val, rtol=TOL, atol=TOL)

    gaps = np.diff(nb_val)
    for k in range(len(nb_val)):
        # only compare where this eigenvalue is nonzero and separated from its neighbours
        left = gaps[k - 1] if k > 0 else np.inf
        right = gaps[k] if k < len(gaps) else np.inf
        if abs(nb_val[k]) < 1e-6 or min(left, right) < 1e-4:
            continue
        dot = float(np.dot(nb_vec[k], rs_vec[k]))
        assert abs(abs(dot) - 1.0) < 1e-5, (
            f"component {k} not parallel (|cos|={abs(dot)})"
        )


def test_the_eigen_equation_holds_for_every_component():
    """The one check immune to sign and degeneracy: cov @ v == lambda * v."""
    c, w = _system(150, 40)
    values, vectors = rb.principal_component_analysis(c, w, backend="rust")
    cov = _covariance(c, w)
    for k in range(len(values)):
        assert np.allclose(
            cov @ vectors[k], values[k] * vectors[k], rtol=0.0, atol=1e-7
        ), f"component {k} violates cov v = lambda v"


def test_rank_deficient_case_agrees_on_eigenvalues_only():
    """n_structures < n_features: a large null space, arbitrary within itself.

    Eigenvalues (including the zeros) must still match; the null-space eigenvectors cannot
    be compared and the test does not try -- it asserts the property instead.
    """
    c, w = _system(50, 40)  # 50 structures, 120 features -> rank <= 50
    nb_val, _ = rb.principal_component_analysis(c, w, backend="numba")
    rs_val, rs_vec = rb.principal_component_analysis(c, w, backend="rust")
    assert np.allclose(nb_val, rs_val, rtol=TOL, atol=TOL), "eigenvalues diverged"
    n_zero = int(np.sum(np.abs(rs_val) < 1e-6))
    assert n_zero >= 120 - 50, "expected a null space from rank deficiency"

    cov = _covariance(c, w)
    for k in range(len(rs_val)):
        assert np.allclose(
            cov @ rs_vec[k], rs_val[k] * rs_vec[k], rtol=0.0, atol=1e-6
        ), f"component {k} violates the eigen equation"


def test_eigenvectors_are_orthonormal_and_sign_stable():
    c, w = _system(300, 30)
    _, first = rb.principal_component_analysis(c, w, backend="rust")
    _, second = rb.principal_component_analysis(c, w, backend="rust")
    assert np.array_equal(first, second), "the Rust result must be reproducible"
    assert np.allclose(first @ first.T, np.eye(first.shape[0]), rtol=0.0, atol=1e-9), (
        "not orthonormal"
    )
    for i in range(first.shape[0]):
        lead = int(np.argmax(np.abs(first[i])))
        assert first[i, lead] > 0.0, f"component {i} not sign-normalised"


def test_variance_is_preserved():
    """Sum of eigenvalues equals the total weighted variance (trace of the covariance)."""
    c, w = _system(200, 35)
    values, _ = rb.principal_component_analysis(c, w, backend="rust")
    assert abs(values.sum() - np.trace(_covariance(c, w))) < 1e-6
