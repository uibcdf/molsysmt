"""
Parity tests for the reusable CSR neighbour-list primitive
(``molsysmt.lib.structure.neighbor_list``) against a brute-force all-pairs
reference that uses the same minimum-image convention as the codebase.
"""

import numpy as np
from molsysmt.lib.structure.neighbor_list import (
    neighbor_list_csr, neighbor_pairs, _mic_wrap_vector)


def _brute(query, ref, cutoff, box=None, exclude_self=True, half=False):
    out = {}
    c2 = cutoff * cutoff
    for i in range(len(query)):
        row = []
        for j in range(len(ref)):
            if exclude_self and j == i:
                continue
            if half and j <= i:
                continue
            dx = ref[j, 0] - query[i, 0]
            dy = ref[j, 1] - query[i, 1]
            dz = ref[j, 2] - query[i, 2]
            if box is not None:
                dx, dy, dz = _mic_wrap_vector(dx, dy, dz, box)
            if dx * dx + dy * dy + dz * dz <= c2:
                row.append(j)
        out[i] = sorted(row)
    return out


def _csr_to_dict(offsets, indices):
    return {i: sorted(indices[offsets[i]:offsets[i + 1]].tolist())
            for i in range(len(offsets) - 1)}


def test_neighbor_list_vacuum_self():
    rng = np.random.default_rng(0)
    x = rng.uniform(0, 3, size=(200, 3))
    off, idx = neighbor_list_csr(x, cutoff=0.7)
    assert _csr_to_dict(off, idx) == _brute(x, x, 0.7)


def test_neighbor_list_vacuum_half():
    rng = np.random.default_rng(1)
    x = rng.uniform(0, 3, size=(200, 3))
    off, idx = neighbor_list_csr(x, cutoff=0.7, half=True)
    assert _csr_to_dict(off, idx) == _brute(x, x, 0.7, half=True)


def test_neighbor_list_vacuum_query_ref_disjoint():
    rng = np.random.default_rng(2)
    x = rng.uniform(0, 3, size=(150, 3))
    y = rng.uniform(0, 3, size=(90, 3))
    off, idx = neighbor_list_csr(x, y, cutoff=0.6, exclude_self=False)
    assert _csr_to_dict(off, idx) == _brute(x, y, 0.6, exclude_self=False)


def test_neighbor_list_pbc_orthogonal():
    rng = np.random.default_rng(3)
    box = np.diag([3.0, 3.0, 3.0]).astype(np.float64)
    x = rng.uniform(0, 3, size=(200, 3))
    off, idx = neighbor_list_csr(x, box=box, cutoff=0.7)
    assert _csr_to_dict(off, idx) == _brute(x, x, 0.7, box=box)


def test_neighbor_list_pbc_triclinic():
    rng = np.random.default_rng(4)
    box = np.array([[3.0, 0.0, 0.0],
                    [0.4, 3.0, 0.0],
                    [0.3, 0.2, 3.0]], dtype=np.float64)
    x = rng.uniform(0, 3, size=(200, 3))
    off, idx = neighbor_list_csr(x, box=box, cutoff=0.6)
    assert _csr_to_dict(off, idx) == _brute(x, x, 0.6, box=box)


def test_neighbor_pairs_half_are_ordered():
    rng = np.random.default_rng(5)
    x = rng.uniform(0, 3, size=(120, 3))
    pairs = neighbor_pairs(x, cutoff=0.7, half=True)
    assert pairs.shape[1] == 2
    assert bool(np.all(pairs[:, 0] < pairs[:, 1]))
    # Same unordered pair set as the brute-force half list.
    brute = _brute(x, x, 0.7, half=True)
    brute_pairs = {(i, j) for i, js in brute.items() for j in js}
    got = {(int(a), int(b)) for a, b in pairs}
    assert got == brute_pairs
