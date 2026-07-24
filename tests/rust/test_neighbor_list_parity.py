"""Parity: Rust neighbor_list_csr_multi vs the Numba oracle (exact).

Skipped unless the optional ``msm_rust_kernels`` wheel is installed. Covers vacuum
and periodic (orthogonal + triclinic), self vs disjoint query/ref, and sorted vs
unsorted, comparing the full flat CSR (offsets, indices, distances) via the opt-in
seam (backend='rust' vs 'numba').
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

RNG = np.random.default_rng(4242)
ORTHO = np.array([[[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]]])
TRIC = np.array([[[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]]])


def _coords(ns, na):
    return np.ascontiguousarray(RNG.uniform(0.0, 6.0, size=(ns, na, 3)))


def _assert_same(a, b):
    off_n, idx_n, d_n = a
    off_r, idx_r, d_r = b
    assert np.array_equal(off_n, off_r)
    assert np.array_equal(idx_n, idx_r)
    assert np.allclose(d_n, d_r, atol=1e-9)


@pytest.mark.parametrize("sort", [True, False], ids=["sorted", "unsorted"])
def test_vacuum_self(sort):
    q = _coords(3, 120)
    nb = rb.neighbor_list_csr_multi(q, cutoff=0.7, exclude_self=True, sort_by_distance=sort, backend="numba")
    rs = rb.neighbor_list_csr_multi(q, cutoff=0.7, exclude_self=True, sort_by_distance=sort, backend="rust")
    _assert_same(nb, rs)


@pytest.mark.parametrize("sort", [True, False], ids=["sorted", "unsorted"])
def test_vacuum_disjoint(sort):
    q, r = _coords(2, 100), _coords(2, 80)
    nb = rb.neighbor_list_csr_multi(q, r, cutoff=0.6, exclude_self=False, sort_by_distance=sort, backend="numba")
    rs = rb.neighbor_list_csr_multi(q, r, cutoff=0.6, exclude_self=False, sort_by_distance=sort, backend="rust")
    _assert_same(nb, rs)


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
@pytest.mark.parametrize("sort", [True, False], ids=["sorted", "unsorted"])
def test_pbc_self(box, sort):
    q = _coords(3, 120)
    b = np.repeat(box, 3, axis=0)
    nb = rb.neighbor_list_csr_multi(q, box=b, cutoff=0.6, exclude_self=True, sort_by_distance=sort, backend="numba")
    rs = rb.neighbor_list_csr_multi(q, box=b, cutoff=0.6, exclude_self=True, sort_by_distance=sort, backend="rust")
    _assert_same(nb, rs)
