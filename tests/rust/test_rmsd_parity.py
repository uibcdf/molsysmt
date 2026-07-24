"""Parity of the Rust RMSD block against the Numba oracle.

`get_rmsd` is a plain reduction, so it only carries the usual `fastmath` gap.

The `least_rmsd` family superposes first, and there parity is at tolerance for three
independent reasons that cannot be engineered away: `fastmath`, a different eigensolver
(`nalgebra` vs LAPACK `dsyevx`), and upstream's `np.sum` for the centroid, which sums
pairwise rather than sequentially. All three are last-bit effects.

The eigenvector's **sign** is not one of those reasons: `q` and `-q` map to the same
rotation matrix, so the kernel's output is well defined and an element-wise tolerance
comparison is valid here. (That is what separates this block from the principal axes,
where the eigenvectors are returned raw and the ambiguity is visible in the result.)

Alongside parity, the superposition is checked against its *defining property* — that
applying the returned rotation and translation actually lands on the reference — which is
a stronger statement than agreeing with Numba.
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

#: The superposition path goes through an eigensolver; 1e-9 is far above the observed gap
#: and far below any physically meaningful difference.
TOL = 1e-9


def _pair(n_structures, n_atoms, seed=2026):
    rng = np.random.default_rng(seed)
    a = np.ascontiguousarray(rng.uniform(-10.0, 10.0, size=(n_structures, n_atoms, 3)))
    b = np.ascontiguousarray(a + rng.normal(0.0, 0.35, size=a.shape))
    return a, b


def _rotate(coords, angle=0.7, shift=(4.0, -3.0, 1.5)):
    c, s = np.cos(angle), np.sin(angle)
    rot = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    return np.ascontiguousarray(coords @ rot.T + np.array(shift))


# ------------------------------------------------------------------------ plain RMSD

@pytest.mark.parametrize("ns", [1, 8], ids=["one-structure", "many-structures"])
def test_get_rmsd(ns):
    c, r = _pair(ns, 400)
    nb = rb.get_rmsd(c, r, backend="numba")
    rs = rb.get_rmsd(c, r, backend="rust")
    assert np.allclose(nb, rs, rtol=TOL, atol=TOL)

    one_nb = rb.get_rmsd_single_structure(c[0], r[0], backend="numba")
    one_rs = rb.get_rmsd_single_structure(c[0], r[0], backend="rust")
    assert abs(one_nb - one_rs) < TOL
    assert abs(one_rs - rs[0]) < TOL


def test_get_rmsd_with_single_reference_structure():
    c, r = _pair(6, 300)
    nb = rb.get_rmsd_with_single_reference_structure(c, r[0], backend="numba")
    rs = rb.get_rmsd_with_single_reference_structure(c, r[0], backend="rust")
    assert np.allclose(nb, rs, rtol=TOL, atol=TOL)
    # must agree with the per-structure kernel fed the same reference
    broadcast = np.ascontiguousarray(np.repeat(r[:1], 6, axis=0))
    assert np.allclose(rs, rb.get_rmsd(c, broadcast, backend="rust"), rtol=TOL, atol=TOL)


def test_plain_rmsd_is_not_blind_to_translation():
    """Guards against accidentally superposing in the kernel that must not."""
    c, _ = _pair(3, 200)
    moved = np.ascontiguousarray(c + np.array([5.0, 0.0, 0.0]))
    assert np.allclose(rb.get_rmsd(c, moved, backend="rust"), 5.0)


# ---------------------------------------------------------------------- least RMSD

@pytest.mark.parametrize("ns", [1, 8], ids=["one-structure", "many-structures"])
def test_get_least_rmsd(ns):
    c, r = _pair(ns, 400)
    nb = rb.get_least_rmsd(c, r, backend="numba")
    rs = rb.get_least_rmsd(c, r, backend="rust")
    assert np.allclose(nb, rs, rtol=TOL, atol=TOL), f"numba {nb} vs rust {rs}"

    one_nb = rb.get_least_rmsd_single_structure(c[0], r[0], backend="numba")
    one_rs = rb.get_least_rmsd_single_structure(c[0], r[0], backend="rust")
    assert abs(one_nb - one_rs) < TOL
    assert abs(one_rs - rs[0]) < TOL


def test_get_least_rmsd_with_single_reference_structure():
    c, r = _pair(6, 300)
    nb = rb.get_least_rmsd_with_single_reference_structure(c, r[0], backend="numba")
    rs = rb.get_least_rmsd_with_single_reference_structure(c, r[0], backend="rust")
    assert np.allclose(nb, rs, rtol=TOL, atol=TOL)


def test_least_rmsd_removes_rigid_body_motion():
    """The property the kernel exists for, asserted directly rather than via Numba."""
    c, _ = _pair(4, 250)
    moved = np.ascontiguousarray(np.stack([_rotate(s) for s in c]))
    rs = rb.get_least_rmsd(c, moved, backend="rust")
    assert np.allclose(rs, 0.0, atol=1e-8), f"rigid motion leaked into the RMSD: {rs}"
    # and the plain RMSD must be large for the same input, or the test proves nothing
    assert rb.get_rmsd(c, moved, backend="rust").min() > 1.0


def test_least_rmsd_never_exceeds_plain_rmsd():
    c, r = _pair(8, 300)
    least = rb.get_least_rmsd(c, r, backend="rust")
    plain = rb.get_rmsd(c, r, backend="rust")
    assert np.all(least <= plain + 1e-12)


# ------------------------------------------------------------- rotation/translation

@pytest.mark.parametrize("ns", [1, 5], ids=["one-structure", "many-structures"])
def test_get_least_rmsd_rotation_and_translation(ns):
    c, r = _pair(ns, 300)
    nb = rb.get_least_rmsd_rotation_and_translation(c, r, backend="numba")
    rs = rb.get_least_rmsd_rotation_and_translation(c, r, backend="rust")
    for name, a, b in zip(("centre", "rotation", "translation"), nb, rs):
        assert a.shape == b.shape, f"{name}: {a.shape} vs {b.shape}"
        assert np.allclose(a, b, rtol=TOL, atol=TOL), f"{name} diverged"
    assert rs[0].shape == (ns, 1, 3)
    assert rs[1].shape == (ns, 1, 3, 3)


def test_rotation_and_translation_single_structure():
    c, r = _pair(1, 300)
    nb = rb.get_least_rmsd_rotation_and_translation_single_structure(
        c[0], r[0], backend="numba")
    rs = rb.get_least_rmsd_rotation_and_translation_single_structure(
        c[0], r[0], backend="rust")
    for a, b in zip(nb, rs):
        assert np.allclose(a, b, rtol=TOL, atol=TOL)
    assert rs[1].shape == (3, 3)


def test_rotation_and_translation_with_single_reference_structure():
    c, r = _pair(5, 250)
    nb = rb.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
        c, r[0], backend="numba")
    rs = rb.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
        c, r[0], backend="rust")
    for a, b in zip(nb, rs):
        assert np.allclose(a, b, rtol=TOL, atol=TOL)


def test_the_returned_transform_actually_superposes():
    """Applies the returned transform and checks it lands on the reference.

    Stronger than parity: it would catch a convention error (a transposed rotation, a
    sign, the wrong centre) that both backends happened to share.
    """
    reference, _ = _pair(3, 200)
    moved = np.ascontiguousarray(np.stack([_rotate(s) for s in reference]))
    centre, rotation, translation = rb.get_least_rmsd_rotation_and_translation(
        moved, reference, backend="rust")
    for s in range(moved.shape[0]):
        centred = moved[s] - centre[s, 0]
        placed = centred @ rotation[s, 0].T + centre[s, 0] + translation[s, 0]
        assert np.allclose(placed, reference[s], atol=1e-8), f"structure {s} did not land"


def test_the_rotation_is_a_proper_rotation():
    """Orthogonal with determinant +1 -- a reflection would also minimise the RMSD."""
    c, r = _pair(4, 200)
    _, rotation, _ = rb.get_least_rmsd_rotation_and_translation(c, r, backend="rust")
    for s in range(c.shape[0]):
        m = rotation[s, 0]
        assert np.allclose(m @ m.T, np.eye(3), atol=1e-10), "not orthogonal"
        assert abs(np.linalg.det(m) - 1.0) < 1e-10, "improper rotation (reflection)"


def test_identical_structures_give_the_identity_transform():
    c, _ = _pair(2, 150)
    centre, rotation, translation = rb.get_least_rmsd_rotation_and_translation(
        c, c, backend="rust")
    for s in range(c.shape[0]):
        assert np.allclose(rotation[s, 0], np.eye(3), atol=1e-9)
        assert np.allclose(translation[s, 0], 0.0, atol=1e-9)
