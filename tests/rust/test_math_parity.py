"""Parity: Rust shared math helpers vs the Numba oracle (molsysmt.lib.math)."""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

RNG = np.random.default_rng(99991)


def _v(n=3):
    return np.ascontiguousarray(RNG.uniform(-2.0, 2.0, size=n))


def test_matmul_and_transpmatmul():
    m = np.ascontiguousarray(RNG.uniform(-1.0, 1.0, size=(3, 3)))
    v = _v()
    assert np.allclose(rb.matmul(m, v, backend="numba"), rb.matmul(m, v, backend="rust"), atol=1e-14)
    assert np.allclose(rb.transpmatmul(m, v, backend="numba"),
                       rb.transpmatmul(m, v, backend="rust"), atol=1e-14)


def test_normalize_vector():
    a = _v()
    nb = rb.normalize_vector(a, backend="numba")
    rs = rb.normalize_vector(a, backend="rust")
    assert np.allclose(nb, rs, atol=1e-14)
    assert np.isclose(np.linalg.norm(rs), 1.0, atol=1e-14)


def test_inverse_matrix_3x3_lower_triangular():
    m = np.array([[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]])
    assert np.allclose(rb.inverse_matrix_3x3(m, backend="numba"),
                       rb.inverse_matrix_3x3(m, backend="rust"), atol=1e-14)


def test_quaternion_to_rotation_matrix():
    q = _v(4)
    q = q / np.linalg.norm(q)
    nb = rb.quaternion_to_rotation_matrix(q, backend="numba")
    rs = rb.quaternion_to_rotation_matrix(q, backend="rust")
    assert np.allclose(nb, rs, atol=1e-14)
    # a unit quaternion must give an orthogonal matrix
    assert np.allclose(rs @ rs.T, np.eye(3), atol=1e-12)


def test_rodrigues_rotation():
    v = _v()
    axis = _v()
    axis = axis / np.linalg.norm(axis)
    ang = 0.7
    nb = rb.rodrigues_rotation(v, axis, ang, backend="numba")
    rs = rb.rodrigues_rotation(v, axis, ang, backend="rust")
    assert np.allclose(nb, rs, atol=1e-14)
    assert np.isclose(np.linalg.norm(rs), np.linalg.norm(v), atol=1e-12)
