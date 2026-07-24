"""Parity: Rust MIC-distance family vs the Numba oracle (bit-for-bit).

Skipped unless the optional ``msm_rust_kernels`` wheel is installed, so it is a
no-op in the normal (Numba-only) CI and an exact-equivalence gate wherever the Rust
accelerator is present. Covers every family member, orthogonal + triclinic boxes,
and multi- vs single-structure shapes, via the opt-in seam (backend='rust' vs 'numba').
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

RNG = np.random.default_rng(20260724)
ORTHO = np.array([[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]])
TRIC = np.array([[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]])


def _coords(ns, na):
    return np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))


def _both(fn, *args):
    return fn(*args, backend="numba"), fn(*args, backend="rust")


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_single_system(box):
    c = _coords(3, 40)
    b = np.stack([box] * 3)
    nb, rs = _both(rb.get_mic_distances_single_system, c, b)
    assert np.allclose(nb, rs, atol=1e-9) and nb.shape == (3, 40, 40)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_two_systems(box):
    c1, c2 = _coords(2, 30), _coords(2, 25)
    b = np.stack([box] * 2)
    nb, rs = _both(rb.get_mic_distances, c1, c2, b)
    assert np.allclose(nb, rs, atol=1e-9) and nb.shape == (2, 30, 25)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_pairs(box):
    c1, c2 = _coords(2, 30), _coords(2, 30)
    b = np.stack([box] * 2)
    nb, rs = _both(rb.get_mic_distances_pairs, c1, c2, b)
    assert np.allclose(nb, rs, atol=1e-9) and nb.shape == (2, 30)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_single_system_single_structure(box):
    c = _coords(1, 50)[0]
    nb, rs = _both(rb.get_mic_distances_single_system_single_structure, c, box)
    assert np.allclose(nb, rs, atol=1e-9) and nb.shape == (50, 50)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_single_structure(box):
    c1, c2 = _coords(1, 40)[0], _coords(1, 35)[0]
    nb, rs = _both(rb.get_mic_distances_single_structure, c1, c2, box)
    assert np.allclose(nb, rs, atol=1e-9) and nb.shape == (40, 35)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_pairs_single_structure(box):
    c1, c2 = _coords(1, 40)[0], _coords(1, 40)[0]
    nb, rs = _both(rb.get_mic_distances_pairs_single_structure, c1, c2, box)
    assert np.allclose(nb, rs, atol=1e-9) and nb.shape == (40,)


def test_backend_flag_semantics():
    c = _coords(1, 10)
    b = np.stack([ORTHO])
    a = rb.get_mic_distances_single_system(c, b, backend="auto")
    r = rb.get_mic_distances_single_system(c, b, backend="rust")
    assert np.array_equal(a, r)  # 'auto' resolves to rust when the wheel is present
