"""Parity: Rust set/shift dihedral edits vs the Numba oracle.

These kernels mutate `coordinates` in place, so parity is checked on the *effect*: the
same input coordinates are edited by each backend and the resulting arrays compared.
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

RNG = np.random.default_rng(13579)
ORTHO = np.array([[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]])
TRIC = np.array([[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]])


def _setup(na=40, n_ang=5):
    coords = np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(na, 3)))
    quartets = np.ascontiguousarray(
        np.stack([RNG.choice(na, size=4, replace=False) for _ in range(n_ang)]).astype(np.int64))
    blocks = np.ascontiguousarray(RNG.random((n_ang, na)) < 0.3)
    angles = np.ascontiguousarray(RNG.uniform(-np.pi, np.pi, size=n_ang))
    return coords, angles, quartets, blocks


def _run(fn, coords, *rest):
    a = np.array(coords, copy=True)
    b = np.array(coords, copy=True)
    fn(a, *rest, backend="numba")
    fn(b, *rest, backend="rust")
    return a, b


def test_shift_dihedral_angles_single_structure():
    coords, angles, quartets, blocks = _setup()
    a, b = _run(rb.shift_dihedral_angles_single_structure, coords, angles, quartets, blocks)
    assert np.allclose(a, b, atol=1e-12)
    assert not np.allclose(a, coords), "the edit must actually move atoms"


def test_set_dihedral_angles_single_structure():
    coords, angles, quartets, blocks = _setup()
    a, b = _run(rb.set_dihedral_angles_single_structure, coords, angles, quartets, blocks)
    assert np.allclose(a, b, atol=1e-12)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_shift_mic_dihedral_angles_single_structure(box):
    coords, angles, quartets, blocks = _setup()
    a = np.array(coords, copy=True)
    b = np.array(coords, copy=True)
    rb.shift_mic_dihedral_angles_single_structure(a, box, angles, quartets, blocks, backend="numba")
    rb.shift_mic_dihedral_angles_single_structure(b, box, angles, quartets, blocks, backend="rust")
    assert np.allclose(a, b, atol=1e-12)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_set_mic_dihedral_angles_single_structure(box):
    coords, angles, quartets, blocks = _setup()
    a = np.array(coords, copy=True)
    b = np.array(coords, copy=True)
    rb.set_mic_dihedral_angles_single_structure(a, box, angles, quartets, blocks, backend="numba")
    rb.set_mic_dihedral_angles_single_structure(b, box, angles, quartets, blocks, backend="rust")
    assert np.allclose(a, b, atol=1e-12)


def test_multi_structure_set_matches_on_well_defined_angles():
    """Fully-shaped angles: the domain where the oracle is defined -> bit parity."""
    na, n_ang, ns = 40, 4, 3
    coords = np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))
    quartets = np.ascontiguousarray(
        np.stack([RNG.choice(na, size=4, replace=False) for _ in range(n_ang)]).astype(np.int64))
    blocks = np.ascontiguousarray(RNG.random((n_ang, na)) < 0.3)
    angles = np.ascontiguousarray(RNG.uniform(-np.pi, np.pi, size=(ns, n_ang)))
    box = np.repeat(ORTHO[np.newaxis, :, :], ns, axis=0)

    a, b = np.array(coords, copy=True), np.array(coords, copy=True)
    rb.set_dihedral_angles(a, angles, quartets, blocks, backend="numba")
    rb.set_dihedral_angles(b, angles, quartets, blocks, backend="rust")
    assert np.allclose(a, b, atol=1e-12)

    a, b = np.array(coords, copy=True), np.array(coords, copy=True)
    rb.set_mic_dihedral_angles(a, box, angles, quartets, blocks, backend="numba")
    rb.set_mic_dihedral_angles(b, box, angles, quartets, blocks, backend="rust")
    assert np.allclose(a, b, atol=1e-12)


def test_broadcast_angles_deliberate_divergence_on_the_periodic_path():
    """Documented, intentional divergence.

    The public API documents `angles` as "compatible with shape (n_structures,
    n_quartets)". The vacuum kernel broadcasts a size-1 dimension; the Numba periodic
    kernel does not and reads out of bounds *without* bounds checking, silently
    returning garbage. Parity is only meaningful where the oracle is defined, so the
    Rust port honours the documented broadcast instead of reproducing undefined
    behaviour. See devguide/pending_bugs/dihedral_angles_broadcast_mismatch_pbc.md.
    """
    na, n_ang, ns = 20, 3, 4
    coords = np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))
    quartets = np.ascontiguousarray(
        np.stack([RNG.choice(na, size=4, replace=False) for _ in range(n_ang)]).astype(np.int64))
    blocks = np.ascontiguousarray(RNG.random((n_ang, na)) < 0.3)
    box = np.repeat(ORTHO[np.newaxis, :, :], ns, axis=0)
    bcast = np.ascontiguousarray(RNG.uniform(-np.pi, np.pi, size=(1, n_ang)))
    full = np.ascontiguousarray(np.repeat(bcast, ns, axis=0))

    # Rust broadcasting must equal Rust with the array explicitly expanded.
    r_bcast, r_full = np.array(coords, copy=True), np.array(coords, copy=True)
    rb.set_mic_dihedral_angles(r_bcast, box, bcast, quartets, blocks, backend="rust")
    rb.set_mic_dihedral_angles(r_full, box, full, quartets, blocks, backend="rust")
    assert np.allclose(r_bcast, r_full, atol=1e-12), "rust must honour the documented broadcast"

    # And it must equal Numba fed the explicitly expanded array (the defined input).
    n_full = np.array(coords, copy=True)
    rb.set_mic_dihedral_angles(n_full, box, full, quartets, blocks, backend="numba")
    assert np.allclose(r_bcast, n_full, atol=1e-12)

    # Numba on the broadcast shape is the undefined case: it neither raises nor matches.
    n_bcast = np.array(coords, copy=True)
    rb.set_mic_dihedral_angles(n_bcast, box, bcast, quartets, blocks, backend="numba")
    assert not np.allclose(n_bcast, n_full, atol=1e-6), (
        "expected the documented upstream defect: numba reads past `angles` and returns "
        "different coordinates instead of broadcasting")


def test_multi_structure_shift_and_set():
    na, n_ang, ns = 40, 4, 3
    coords = np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))
    quartets = np.ascontiguousarray(
        np.stack([RNG.choice(na, size=4, replace=False) for _ in range(n_ang)]).astype(np.int64))
    blocks = np.ascontiguousarray(RNG.random((n_ang, na)) < 0.3)
    angles = np.ascontiguousarray(RNG.uniform(-np.pi, np.pi, size=(ns, n_ang)))
    idx = np.ascontiguousarray(np.arange(ns, dtype=np.int64))
    a = np.array(coords, copy=True)
    b = np.array(coords, copy=True)
    rb.shift_dihedral_angles(a, angles, quartets, blocks, idx, backend="numba")
    rb.shift_dihedral_angles(b, angles, quartets, blocks, idx, backend="rust")
    assert np.allclose(a, b, atol=1e-12)
