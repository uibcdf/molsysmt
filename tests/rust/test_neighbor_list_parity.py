"""Parity: Rust neighbor-list membership exactly and distances within a tight envelope.

Requires the private ``molsysmt._rust`` extension built into MolSysMT. Covers vacuum
and periodic (orthogonal + triclinic), self vs disjoint query/ref, and sorted vs
unsorted, comparing exact CSR offsets and indices plus bounded floating distances via
the opt-in seam (backend='rust' vs 'numba').
"""

import numpy as np
import pytest

import molsysmt._rust  # noqa: F401, E402

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
    assert np.allclose(d_n, d_r, rtol=0.0, atol=1e-9)


@pytest.mark.parametrize("sort", [True, False], ids=["sorted", "unsorted"])
def test_vacuum_self(sort):
    q = _coords(3, 120)
    nb = rb.neighbor_list_csr_multi(
        q, cutoff=0.7, exclude_self=True, sort_by_distance=sort, backend="numba"
    )
    rs = rb.neighbor_list_csr_multi(
        q, cutoff=0.7, exclude_self=True, sort_by_distance=sort, backend="rust"
    )
    _assert_same(nb, rs)


@pytest.mark.parametrize("sort", [True, False], ids=["sorted", "unsorted"])
def test_vacuum_disjoint(sort):
    q, r = _coords(2, 100), _coords(2, 80)
    nb = rb.neighbor_list_csr_multi(
        q, r, cutoff=0.6, exclude_self=False, sort_by_distance=sort, backend="numba"
    )
    rs = rb.neighbor_list_csr_multi(
        q, r, cutoff=0.6, exclude_self=False, sort_by_distance=sort, backend="rust"
    )
    _assert_same(nb, rs)


def _ground_truth_pairs(coords, box, cutoff):
    """True neighbour set by the minimum image over a wide (±2) all-pairs search."""
    na = coords.shape[0]
    inv = np.linalg.inv(box)
    d = coords[None, :, :] - coords[:, None, :]
    s = d @ inv
    base = np.round(s)
    best = np.full((na, na), np.inf)
    for i in range(-2, 3):
        for j in range(-2, 3):
            for k in range(-2, 3):
                w = (s - (base + [i, j, k])) @ box
                best = np.minimum(best, (w * w).sum(-1))
    best = np.sqrt(best)
    np.fill_diagonal(best, np.inf)
    return set(map(tuple, np.argwhere(best <= cutoff)))


def _rust_pairs(off, idx, na):
    return {(i, int(idx[p])) for i in range(na) for p in range(off[i], off[i + 1])}


@pytest.mark.parametrize("box", [ORTHO, TRIC], ids=["orthogonal", "triclinic"])
@pytest.mark.parametrize("sort", [True, False], ids=["sorted", "unsorted"])
def test_pbc_self(box, sort):
    q = _coords(3, 120)
    b = np.repeat(box, 3, axis=0)
    rs = rb.neighbor_list_csr_multi(
        q, box=b, cutoff=0.6, exclude_self=True, sort_by_distance=sort, backend="rust"
    )
    if box is ORTHO:
        # orthogonal: Rust and Numba are both correct and bit-for-bit
        nb = rb.neighbor_list_csr_multi(
            q,
            box=b,
            cutoff=0.6,
            exclude_self=True,
            sort_by_distance=sort,
            backend="numba",
        )
        _assert_same(nb, rs)
    else:
        # triclinic: Rust matches the true minimum-image neighbours exactly, and Numba does
        # not (its cell list mis-bins the skewed grid and its wrap is single-image). This
        # is the correctness fix; see triclinic_cell_list_completeness.md.
        off, idx, _ = rs
        rs_pairs = _rust_pairs(off, idx, 120)
        truth = _ground_truth_pairs(q[0], box[0], 0.6)
        assert rs_pairs == truth, (
            f"rust missing {len(truth - rs_pairs)}, extra {len(rs_pairs - truth)}"
        )
        nb = rb.neighbor_list_csr_multi(
            q,
            box=b,
            cutoff=0.6,
            exclude_self=True,
            sort_by_distance=sort,
            backend="numba",
        )
        nb_pairs = _rust_pairs(nb[0], nb[1], 120)
        assert nb_pairs != truth, (
            "Numba now matches the true neighbours -- retire this split"
        )
