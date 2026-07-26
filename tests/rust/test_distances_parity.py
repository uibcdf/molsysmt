"""Parity: Rust distance family vs the Numba oracle within an absolute envelope.

Skipped unless the optional ``msm_rust_kernels`` wheel is installed. Covers every
family member and both shapes (multi- and single-structure), via the opt-in seam.
This is the vacuum counterpart of test_mic_distances_parity.py.
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

RNG = np.random.default_rng(161803)


def _coords(ns, na):
    return np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))


def _both(fn, *args):
    return fn(*args, backend="numba"), fn(*args, backend="rust")


def test_single_system():
    c = _coords(3, 60)
    nb, rs = _both(rb.get_distances_single_system, c)
    assert nb.shape == (3, 60, 60)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)
    # the matrix must be symmetric with a zero diagonal
    assert np.allclose(rs, np.transpose(rs, (0, 2, 1)), rtol=0.0, atol=1e-12)
    assert np.allclose(
        np.einsum("sii->si", rs), 0.0, rtol=0.0, atol=1e-12
    )


def test_two_systems():
    c1, c2 = _coords(2, 40), _coords(2, 30)
    nb, rs = _both(rb.get_distances, c1, c2)
    assert nb.shape == (2, 40, 30)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


def test_pairs():
    c1, c2 = _coords(2, 50), _coords(2, 50)
    nb, rs = _both(rb.get_distances_pairs, c1, c2)
    assert nb.shape == (2, 50)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


def test_single_system_single_structure():
    c = _coords(1, 70)[0]
    nb, rs = _both(rb.get_distances_single_system_single_structure, c)
    assert nb.shape == (70, 70)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


def test_single_structure():
    c1, c2 = _coords(1, 45)[0], _coords(1, 35)[0]
    nb, rs = _both(rb.get_distances_single_structure, c1, c2)
    assert nb.shape == (45, 35)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


def test_pairs_single_structure():
    c1, c2 = _coords(1, 45)[0], _coords(1, 45)[0]
    nb, rs = _both(rb.get_distances_pairs_single_structure, c1, c2)
    assert nb.shape == (45,)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)
