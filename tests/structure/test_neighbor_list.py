"""
Parity tests for the reusable CSR neighbour-list primitive
(``molsysmt.lib.structure.neighbor_list``) against a brute-force all-pairs
reference that uses the same minimum-image convention as the codebase.
"""

import numpy as np
from molsysmt.lib.structure.neighbor_list import (
    neighbor_list_csr, neighbor_pairs, neighbor_list_csr_multi, _mic_wrap_vector)


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


def test_neighbor_list_return_distances_matches_brute():
    rng = np.random.default_rng(6)
    x = rng.uniform(0, 3, size=(200, 3))
    box = np.array([[3.0, 0.0, 0.0],
                    [0.3, 3.0, 0.0],
                    [0.2, 0.1, 3.0]], dtype=np.float64)
    for kw in ({}, {'box': box}):
        off, idx, dist = neighbor_list_csr(x, cutoff=0.6, return_distances=True, **kw)
        for i in range(len(x)):
            for p in range(off[i], off[i + 1]):
                dv = x[idx[p]] - x[i]
                if 'box' in kw:
                    dv = np.array(_mic_wrap_vector(dv[0], dv[1], dv[2], box))
                assert np.isclose(np.linalg.norm(dv), dist[p], atol=1e-9)
    # Default call stays a 2-tuple (backward compatible).
    assert len(neighbor_list_csr(x, cutoff=0.6)) == 2


def _multi_sets(offsets, indices, n_query):
    return {(w // n_query, w % n_query): set(indices[offsets[w]:offsets[w + 1]].tolist())
            for w in range(len(offsets) - 1)}


def test_neighbor_list_csr_multi_matches_brute():
    rng = np.random.default_rng(11)
    ns, nq = 3, 120
    q = rng.uniform(0, 3, size=(ns, nq, 3))
    box = np.stack([np.array([[3.0, 0, 0], [0.3, 3.0, 0], [0.2, 0.1, 3.0]])] * ns)

    def brute(query, ref, cutoff, box=None, excl=True):
        out = {}
        for s in range(query.shape[0]):
            for i in range(query.shape[1]):
                row = []
                for j in range(ref.shape[1]):
                    if excl and j == i:
                        continue
                    d = ref[s, j] - query[s, i]
                    if box is not None:
                        d = np.array(_mic_wrap_vector(d[0], d[1], d[2], box[s]))
                    if d @ d <= cutoff * cutoff:
                        row.append(j)
                out[(s, i)] = set(row)
        return out

    # self, vacuum, sorted by distance
    off, idx, dist = neighbor_list_csr_multi(q, cutoff=0.6, sort_by_distance=True)
    assert _multi_sets(off, idx, nq) == brute(q, q, 0.6)
    for w in range(len(off) - 1):
        s, i = w // nq, w % nq
        dd = dist[off[w]:off[w + 1]]
        assert np.all(np.diff(dd) >= -1e-9)
        for p in range(off[w], off[w + 1]):
            assert np.isclose(np.linalg.norm(q[s, idx[p]] - q[s, i]), dist[p], atol=1e-9)

    # disjoint sets, vacuum
    r = rng.uniform(0, 3, size=(ns, 90, 3))
    off, idx, _ = neighbor_list_csr_multi(q, r, cutoff=0.6, exclude_self=False)
    assert _multi_sets(off, idx, nq) == brute(q, r, 0.6, excl=False)

    # self, PBC
    off, idx, _ = neighbor_list_csr_multi(q, box=box, cutoff=0.6)
    assert _multi_sets(off, idx, nq) == brute(q, q, 0.6, box=box)


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
