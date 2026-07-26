"""Parity: Rust angle family vs the Numba oracle within an absolute envelope.

Skipped unless the optional ``msm_rust_kernels`` wheel is installed. Covers vacuum and
periodic (orthogonal + triclinic) angles, multi- and single-structure, via the opt-in
seam. `get_angles` is on the hbonds.get_luzard_chandler_hbonds path.
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

RNG = np.random.default_rng(2718)
ORTHO = np.array([[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]])
TRIC = np.array([[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]])


def _setup(ns, na, nt):
    coords = np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))
    triplets = np.ascontiguousarray(
        np.stack([RNG.choice(na, size=3, replace=False) for _ in range(nt)]).astype(
            np.int64
        )
    )
    return coords, triplets


def test_angles_multi_structure():
    coords, triplets = _setup(4, 60, 200)
    nb = rb.get_angles(coords, triplets, backend="numba")
    rs = rb.get_angles(coords, triplets, backend="rust")
    assert nb.shape == (4, 200)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


def test_angles_single_structure():
    coords, triplets = _setup(1, 60, 200)
    nb = rb.get_angles_single_structure(coords[0], triplets, backend="numba")
    rs = rb.get_angles_single_structure(coords[0], triplets, backend="rust")
    assert nb.shape == (200,)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_mic_angles_multi_structure(box):
    coords, triplets = _setup(3, 60, 200)
    b = np.stack([box] * 3)
    nb = rb.get_mic_angles(coords, b, triplets, backend="numba")
    rs = rb.get_mic_angles(coords, b, triplets, backend="rust")
    assert nb.shape == (3, 200)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_mic_angles_single_structure(box):
    coords, triplets = _setup(1, 60, 200)
    nb = rb.get_mic_angles_single_structure(coords[0], box, triplets, backend="numba")
    rs = rb.get_mic_angles_single_structure(coords[0], box, triplets, backend="rust")
    assert nb.shape == (200,)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)
