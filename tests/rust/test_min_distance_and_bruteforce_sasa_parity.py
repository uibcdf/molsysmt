"""Parity of the last four ported kernels: the two minimum-distance kernels and the
brute-force (non cell-list) SASA kernels.

The minimum-distance kernels are integer-masked reductions returning a single distance, so
they are bit-for-bit. The brute-force SASA carries the usual tolerance: `fastmath` reorders
the final `4·π·r²·(count/n_points)`, so even the vacuum kernel differs at ~1e-16 (the
occlusion counts are identical — a flipped count would show up as a ~1e-3 jump, not seen).
The MIC kernel additionally corrects the same `_is_orthogonal` typo as the cell-list
version, agreeing to ~1e-15 on a cubic box rather than exactly (see
`devguide/pending_bugs/sasa_is_orthogonal_typo.md`).
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402
from molsysmt.lib.structure.get_sasa_cuda import get_fibonacci_sphere_points  # noqa: E402


# --------------------------------------------------------------- minimum distance


def _bonded_matrix(n, pairs, seed=0):
    b = np.zeros((n, n), dtype=np.uint8)
    for i, j in pairs:
        b[i, j] = 1
        b[j, i] = 1
    return np.ascontiguousarray(b)


def test_minimum_distance_masked_not_bonded():
    rng = np.random.default_rng(1)
    n = 60
    coords = np.ascontiguousarray(rng.uniform(-5, 5, size=(n, 3)))
    mask = np.ascontiguousarray((rng.random(n) > 0.2).astype(np.uint8))
    bonded = _bonded_matrix(n, [(0, 1), (2, 3), (5, 9), (10, 11)])
    nb = rb.minimum_distance_masked_not_bonded(coords, mask, bonded, backend="numba")
    rs = rb.minimum_distance_masked_not_bonded(coords, mask, bonded, backend="rust")
    assert nb == rs, f"numba {nb} vs rust {rs}"


def test_minimum_distance_masked_returns_inf_when_no_admissible_pair():
    coords = np.ascontiguousarray(np.zeros((3, 3)))
    mask = np.array([1, 0, 0], dtype=np.uint8)  # only one included atom
    bonded = np.zeros((3, 3), dtype=np.uint8)
    nb = rb.minimum_distance_masked_not_bonded(coords, mask, bonded, backend="numba")
    rs = rb.minimum_distance_masked_not_bonded(coords, mask, bonded, backend="rust")
    assert np.isinf(nb) and np.isinf(rs)


def test_minimum_distance_between_coordinate_sets():
    rng = np.random.default_rng(2)
    ne, nc = 40, 25
    existing = np.ascontiguousarray(rng.uniform(-5, 5, size=(ne, 3)))
    candidate = np.ascontiguousarray(rng.uniform(-5, 5, size=(nc, 3)))
    emask = np.ascontiguousarray((rng.random(ne) > 0.2).astype(np.uint8))
    cmask = np.ascontiguousarray((rng.random(nc) > 0.2).astype(np.uint8))
    start = ne
    # shape (ne, ne + nc), indexed [existing_index, candidate_global_index] — not square
    bonded = np.zeros((ne, ne + nc), dtype=np.uint8)
    bonded[0, start + 0] = 1
    bonded[3, start + 4] = 1
    bonded = np.ascontiguousarray(bonded)
    nb = rb.minimum_distance_between_coordinate_sets(
        existing, emask, candidate, cmask, start, bonded, backend="numba"
    )
    rs = rb.minimum_distance_between_coordinate_sets(
        existing, emask, candidate, cmask, start, bonded, backend="rust"
    )
    assert nb == rs, f"numba {nb} vs rust {rs}"


def test_minimum_distance_between_sets_matches_a_brute_python_check():
    """Independent oracle: the reported distance must be the true masked/non-bonded min."""
    rng = np.random.default_rng(3)
    ne, nc = 20, 15
    existing = np.ascontiguousarray(rng.uniform(-4, 4, size=(ne, 3)))
    candidate = np.ascontiguousarray(rng.uniform(-4, 4, size=(nc, 3)))
    emask = np.ones(ne, dtype=np.uint8)
    cmask = np.ones(nc, dtype=np.uint8)
    bonded = np.zeros((ne, ne + nc), dtype=np.uint8)
    rs = rb.minimum_distance_between_coordinate_sets(
        existing, emask, candidate, cmask, ne, bonded, backend="rust"
    )
    truth = min(
        np.linalg.norm(existing[i] - candidate[j]) for i in range(ne) for j in range(nc)
    )
    assert abs(rs - truth) < 1e-12


# ------------------------------------------------------------- brute-force SASA

ORTHO = np.array([[[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]]])
TRIC = np.array([[[6.0, 0.0, 0.0], [1.5, 6.5, 0.0], [0.8, 1.1, 7.0]]])


def _sasa_setup(ns, na, seed=7):
    rng = np.random.default_rng(seed)
    coords = np.ascontiguousarray(rng.uniform(0, 6, size=(ns, na, 3)))
    radii = np.ascontiguousarray(rng.uniform(0.12, 0.20, size=na))
    sphere = np.ascontiguousarray(get_fibonacci_sphere_points(120))
    return coords, radii, sphere, 0.14


@pytest.mark.parametrize("ns", [1, 3], ids=["one-structure", "many-structures"])
def test_get_sasa_bruteforce_vacuum(ns):
    coords, radii, sphere, probe = _sasa_setup(ns, 80)
    nb = rb.get_sasa(coords, radii, sphere, probe, backend="numba")
    rs = rb.get_sasa(coords, radii, sphere, probe, backend="rust")
    assert nb.shape == (ns, 80)
    # tolerance, not equality: fastmath reorders the final 4*pi*r^2*(count/n) product; the
    # occlusion counts match (a flipped count would be a ~1e-3 jump, not ~1e-16).
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-9), (
        "vacuum brute-force SASA beyond the fastmath gap"
    )


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
def test_get_mic_sasa_bruteforce(box):
    coords, radii, sphere, probe = _sasa_setup(2, 80)
    b = np.ascontiguousarray(np.repeat(box, 2, axis=0))
    nb = rb.get_mic_sasa(coords, b, radii, sphere, probe, backend="numba")
    rs = rb.get_mic_sasa(coords, b, radii, sphere, probe, backend="rust")
    # tolerance, not equality: the corrected _is_orthogonal makes the cubic-box branches
    # agree to ~1e-15 rather than bit-for-bit (documented deliberate correction).
    assert np.allclose(nb, rs, rtol=0.0, atol=1e-9), (
        "MIC brute-force SASA beyond the expected gap"
    )


def test_bruteforce_and_cell_list_sasa_agree():
    """The two SASA implementations must give the same answer (cross-check, not parity)."""
    coords, radii, sphere, probe = _sasa_setup(1, 120)
    cutoff = 2.0 * float(radii.max()) + 2.0 * probe
    brute = rb.get_sasa(coords, radii, sphere, probe, backend="rust")
    cell = rb.get_sasa_cell_list(coords, radii, sphere, probe, cutoff, backend="rust")
    assert np.allclose(brute, cell, rtol=0.0, atol=1e-9), (
        "cell-list and brute-force SASA disagree"
    )
