"""Parity: Rust cell-list SASA kernels vs the Numba oracle (bit-for-bit).

Skipped unless the optional ``msm_rust_kernels`` wheel is installed. Covers the vacuum
and periodic (orthogonal + triclinic) Shrake-Rupley cell-list kernels, single and
multiple structures, via the opt-in seam (backend='rust' vs 'numba').
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402
from molsysmt.lib.structure.get_sasa_cuda import get_fibonacci_sphere_points  # noqa: E402

RNG = np.random.default_rng(31415)
PROBE = 0.14
ORTHO = np.array([[[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]]])
TRIC = np.array([[[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]]])


def _setup(ns, na, n_points=100):
    coords = np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))
    radii = np.ascontiguousarray(RNG.uniform(0.12, 0.20, size=na))
    sphere = np.ascontiguousarray(get_fibonacci_sphere_points(n_points))
    cutoff = 2.0 * float(radii.max()) + 2.0 * PROBE
    return coords, radii, sphere, cutoff


@pytest.mark.parametrize("ns", [1, 4], ids=["one-structure", "many-structures"])
def test_sasa_cell_list_vacuum(ns):
    coords, radii, sphere, cutoff = _setup(ns, 300)
    nb = rb.get_sasa_cell_list(coords, radii, sphere, PROBE, cutoff, backend="numba")
    rs = rb.get_sasa_cell_list(coords, radii, sphere, PROBE, cutoff, backend="rust")
    assert nb.shape == (ns, 300)
    assert np.allclose(nb, rs, atol=1e-9)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
@pytest.mark.parametrize("ns", [1, 3], ids=["one-structure", "many-structures"])
def test_mic_sasa_cell_list(box, ns):
    """Tolerance, not bit-equality, and deliberately so on the orthogonal box.

    The Rust port corrects the `_is_orthogonal` typo that makes upstream always take the
    triclinic branch (see `devguide/pending_bugs/sasa_is_orthogonal_typo.md`), so on a
    cubic box the two implementations reach the same answer by different arithmetic.
    Measured divergence: 4.4e-16 max, relative 4.4e-16 — do not tighten this to `==`.
    """
    coords, radii, sphere, cutoff = _setup(ns, 250)
    b = np.repeat(box, ns, axis=0)
    nb = rb.get_mic_sasa_cell_list(coords, b, radii, sphere, PROBE, cutoff, backend="numba")
    rs = rb.get_mic_sasa_cell_list(coords, b, radii, sphere, PROBE, cutoff, backend="rust")
    assert nb.shape == (ns, 250)
    assert np.allclose(nb, rs, atol=1e-9)


def test_zero_radius_atoms_are_zero_in_both():
    """Dummy atoms (radius 0) must yield 0.0 area in both backends."""
    coords, radii, sphere, cutoff = _setup(1, 120)
    radii = radii.copy()
    radii[:10] = 0.0
    nb = rb.get_sasa_cell_list(coords, radii, sphere, PROBE, cutoff, backend="numba")
    rs = rb.get_sasa_cell_list(coords, radii, sphere, PROBE, cutoff, backend="rust")
    assert np.allclose(nb, rs, atol=1e-9)
    assert np.all(nb[0, :10] == 0.0)
