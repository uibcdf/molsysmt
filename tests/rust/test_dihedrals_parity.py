"""Parity: Rust dihedral-angle family vs the Numba oracle within an absolute envelope.

Requires the private ``molsysmt._rust`` extension built into MolSysMT. Covers vacuum and
periodic (orthogonal + triclinic), multi- and single-structure, via the opt-in seam.
The sign convention (negated when cross(aux0,aux1)·vect1 <= 0) is part of the contract,
so the comparison is signed, not on magnitudes.
"""

import numpy as np
import pytest

import molsysmt._rust  # noqa: F401, E402

from molsysmt._private import rust_backend as rb  # noqa: E402

RNG = np.random.default_rng(577215)
ORTHO = np.array([[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]])
TRIC = np.array([[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]])


def _setup(ns, na, nq):
    coords = np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))
    quartets = np.ascontiguousarray(
        np.stack([RNG.choice(na, size=4, replace=False) for _ in range(nq)]).astype(
            np.int64
        )
    )
    return coords, quartets


def test_dihedrals_multi_structure():
    coords, quartets = _setup(4, 50, 150)
    nb = rb.get_dihedral_angles(coords, quartets, backend="numba")
    rs = rb.get_dihedral_angles(coords, quartets, backend="rust")
    assert nb.shape == (4, 150)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)
    # signed contract: both backends must agree on sign, not just magnitude
    assert np.array_equal(np.sign(nb), np.sign(rs))


def test_dihedrals_single_structure():
    coords, quartets = _setup(1, 50, 150)
    nb = rb.get_dihedral_angles_single_structure(coords[0], quartets, backend="numba")
    rs = rb.get_dihedral_angles_single_structure(coords[0], quartets, backend="rust")
    assert nb.shape == (150,)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_mic_dihedrals_multi_structure(box):
    coords, quartets = _setup(3, 50, 150)
    b = np.stack([box] * 3)
    nb = rb.get_mic_dihedral_angles(coords, b, quartets, backend="numba")
    rs = rb.get_mic_dihedral_angles(coords, b, quartets, backend="rust")
    assert nb.shape == (3, 150)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_mic_dihedrals_single_structure(box):
    coords, quartets = _setup(1, 50, 150)
    nb = rb.get_mic_dihedral_angles_single_structure(
        coords[0], box, quartets, backend="numba"
    )
    rs = rb.get_mic_dihedral_angles_single_structure(
        coords[0], box, quartets, backend="rust"
    )
    assert nb.shape == (150,)
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-12)
