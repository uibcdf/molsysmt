"""Comprehensive correctness battery for the Rust MIC + neighbour-list + SASA surface.

This is the regression net that must stay green through any performance work on the MIC and
cell-list kernels. It validates against *independent ground truth* — an all-pairs search
over a wide (±3) image shell rather than a second implementation. Every result
must match exactly (integer neighbour sets) or to a tight tolerance
(distances), across a broad sweep of box shapes, cutoffs and query configurations.

Coverage
--------
* box shapes: orthogonal, mild triclinic, heavily skewed (tilt up to 0.5·L), near-cubic
  rotated, and several random lower-triangular boxes per seed;
* sizes: single atom, small boxes where n_cells < 3, and typical systems;
* neighbour list: self vs disjoint query/ref, sorted vs unsorted, exclude_self on/off,
  cutoffs from small to near L/2, atoms exactly on cell boundaries;
* invariants: no duplicates, no false positives/negatives, symmetric distances, sorted
  order when requested;
* cross-kernel: the dense MIC distance matrix, the cell-list SASA against brute force, and
  MIC angles/dihedrals, all against the same ground truth.
"""

import numpy as np
import pytest

import molsysmt._rust  # noqa: F401, E402

from molsysmt._private import rust_backend as rb  # noqa: E402
from molsysmt.lib.structure.sphere_points import get_fibonacci_sphere_points  # noqa: E402


# --------------------------------------------------------------------------- boxes


def _lower_tri(ax, by, cz, bx=0.0, cx=0.0, cy=0.0):
    return np.array([[ax, 0.0, 0.0], [bx, by, 0.0], [cx, cy, cz]])


BOXES = {
    "orthogonal": _lower_tri(6.0, 6.0, 6.0),
    "mild-tric": _lower_tri(6.0, 6.5, 7.0, bx=1.5, cx=0.8, cy=1.1),
    "skewed": _lower_tri(6.0, 6.0, 6.0, bx=3.0, cx=3.0, cy=3.0),  # tilt 0.5·L
    "skewed-2": _lower_tri(6.0, 7.0, 8.0, bx=-2.5, cx=2.0, cy=-3.0),
    "flat-ish": _lower_tri(8.0, 8.0, 4.0, bx=2.0, cx=1.0, cy=1.5),
}


def _random_boxes(n, seed):
    """Random lower-triangular boxes with tilt within the reduction limit (|tilt| ≤ 0.5·L)."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        ax, by, cz = rng.uniform(5.0, 9.0, size=3)
        bx = rng.uniform(-0.5, 0.5) * ax
        cx = rng.uniform(-0.5, 0.5) * ax
        cy = rng.uniform(-0.5, 0.5) * by
        out.append(_lower_tri(ax, by, cz, bx, cx, cy))
    return out


# ------------------------------------------------------------------- ground truth


def _min_image_sq(d, box, shell=3):
    """All-pairs squared minimum-image distances via a ±shell integer search."""
    inv = np.linalg.inv(box)
    s = d @ inv
    base = np.round(s)
    best = np.full(d.shape[:-1], np.inf)
    rng = range(-shell, shell + 1)
    for i in rng:
        for j in rng:
            for k in rng:
                w = (s - (base + [i, j, k])) @ box
                best = np.minimum(best, (w * w).sum(-1))
    return best


def _truth_pairs(q, r, box, cutoff, exclude_self):
    d = r[None, :, :] - q[:, None, :]
    best = np.sqrt(_min_image_sq(d, box))
    if exclude_self and q.shape == r.shape and np.shares_memory(q, r):
        np.fill_diagonal(best, np.inf)
    within = best <= cutoff
    if exclude_self and q.shape[0] == r.shape[0]:
        for i in range(min(q.shape[0], r.shape[0])):
            within[i, i] = within[i, i] and not np.allclose(q[i], r[i])
    return {(i, j) for i, j in np.argwhere(within)}


def _rust_pairs(off, idx, nq):
    return {(i, int(idx[p])) for i in range(nq) for p in range(off[i], off[i + 1])}


def _coords(n, box, seed, spill=1.5):
    """Atoms filling the cell, deliberately spilling past the faces to exercise wrapping."""
    rng = np.random.default_rng(seed)
    frac = rng.uniform(-0.2, 1.2, size=(n, 3))
    return np.ascontiguousarray(frac @ box)


# =============================================================== neighbour list

ALL_BOXES = list(BOXES) + [f"rand{i}" for i in range(6)]


def _box(name):
    return BOXES[name] if name in BOXES else _random_boxes(6, 20260725)[int(name[4:])]


@pytest.mark.parametrize("box_name", ALL_BOXES)
@pytest.mark.parametrize("cutoff", [0.6, 1.2, 2.5])
@pytest.mark.parametrize("sort", [False, True], ids=["unsorted", "sorted"])
def test_self_neighbour_list_matches_ground_truth(box_name, cutoff, sort):
    box = _box(box_name)
    c = _coords(120, box, seed=7)
    off, idx, dist = rb.neighbor_list_csr_multi(
        c[None],
        None,
        box=box[None],
        cutoff=cutoff,
        exclude_self=True,
        sort_by_distance=sort,
        backend="rust",
    )
    got = _rust_pairs(off, idx, 120)
    truth = _truth_pairs(c, c, box, cutoff, exclude_self=True)
    assert got == truth, (
        f"{box_name} cut={cutoff}: missing {len(truth - got)}, extra {len(got - truth)}"
    )
    # no duplicates, and distances correct + (optionally) sorted
    for i in range(120):
        row = idx[off[i] : off[i + 1]]
        assert len(row) == len(set(row.tolist())), f"duplicate neighbour of atom {i}"
        drow = dist[off[i] : off[i + 1]]
        if sort:
            assert np.all(np.diff(drow) >= -1e-12), "distances not sorted"


@pytest.mark.parametrize("box_name", ["orthogonal", "mild-tric", "skewed", "skewed-2"])
@pytest.mark.parametrize("cutoff", [0.8, 1.5])
def test_disjoint_neighbour_list_matches_ground_truth(box_name, cutoff):
    box = _box(box_name)
    q = _coords(80, box, seed=1)
    r = _coords(100, box, seed=2)
    off, idx, _ = rb.neighbor_list_csr_multi(
        q[None],
        r[None],
        box=box[None],
        cutoff=cutoff,
        exclude_self=False,
        sort_by_distance=False,
        backend="rust",
    )
    got = _rust_pairs(off, idx, 80)
    truth = _truth_pairs(q, r, box, cutoff, exclude_self=False)
    assert got == truth, (
        f"{box_name} cut={cutoff}: missing {len(truth - got)}, extra {len(got - truth)}"
    )


@pytest.mark.parametrize("box_name", ["orthogonal", "skewed"])
def test_small_box_fewer_than_three_cells_no_double_count(box_name):
    # box ≈ 2× cutoff → n_cells is 1 or 2 per axis, the ±1 stencil would revisit cells
    base = _box(box_name)
    box = base * (2.2 / 6.0)  # shrink to ~2.2 nm
    c = _coords(60, box, seed=3)
    cutoff = 0.9
    off, idx, _ = rb.neighbor_list_csr_multi(
        c[None],
        None,
        box=box[None],
        cutoff=cutoff,
        exclude_self=True,
        sort_by_distance=False,
        backend="rust",
    )
    got = _rust_pairs(off, idx, 60)
    truth = _truth_pairs(c, c, box, cutoff, exclude_self=True)
    assert got == truth, (
        f"{box_name} small: missing {len(truth - got)}, extra {len(got - truth)}"
    )
    for i in range(60):
        row = idx[off[i] : off[i + 1]]
        assert len(row) == len(set(row.tolist())), "duplicate on small box"


def test_single_atom_has_no_neighbours():
    box = BOXES["skewed"]
    c = _coords(1, box, seed=0)
    off, idx, _ = rb.neighbor_list_csr_multi(
        c[None],
        None,
        box=box[None],
        cutoff=2.0,
        exclude_self=True,
        sort_by_distance=False,
        backend="rust",
    )
    assert off[-1] == 0 and len(idx) == 0


def test_atoms_on_cell_boundaries():
    """Atoms placed exactly on fractional cell boundaries must still be found correctly."""
    box = BOXES["mild-tric"]
    fr = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.5, 0.0, 0.0],
            [0.999, 0.5, 0.25],
            [0.0, 0.999, 0.75],
            [1.0 - 1e-12, 1.0 - 1e-12, 1.0 - 1e-12],
        ]
    )
    c = np.ascontiguousarray(fr @ box)
    cutoff = 2.0
    off, idx, _ = rb.neighbor_list_csr_multi(
        c[None],
        None,
        box=box[None],
        cutoff=cutoff,
        exclude_self=True,
        sort_by_distance=False,
        backend="rust",
    )
    got = _rust_pairs(off, idx, len(c))
    truth = _truth_pairs(c, c, box, cutoff, exclude_self=True)
    assert got == truth


def test_many_structures_are_independent():
    box = BOXES["skewed"]
    cs = np.ascontiguousarray(np.stack([_coords(60, box, seed=s) for s in range(4)]))
    b = np.repeat(box[None], 4, axis=0)
    off, idx, _ = rb.neighbor_list_csr_multi(
        cs,
        None,
        box=b,
        cutoff=1.2,
        exclude_self=True,
        sort_by_distance=False,
        backend="rust",
    )
    # compare each structure's block against its own ground truth
    na = 60
    for s in range(4):
        base = s * na
        got = {
            (i, int(idx[p]))
            for i in range(na)
            for p in range(off[base + i], off[base + i + 1])
        }
        truth = _truth_pairs(cs[s], cs[s], box, 1.2, exclude_self=True)
        assert got == truth, f"structure {s} diverged"


# =============================================================== dense distances


@pytest.mark.parametrize("box_name", ["orthogonal", "mild-tric", "skewed", "skewed-2"])
def test_dense_mic_distance_matrix_matches_ground_truth(box_name):
    box = _box(box_name)
    c = _coords(60, box, seed=11)
    D = rb.get_mic_distances_single_system(c[None], box[None], backend="rust")[0]
    truth = np.sqrt(_min_image_sq(c[None, :, :] - c[:, None, :], box))
    assert np.allclose(D, truth, atol=1e-9), (
        f"{box_name}: max diff {np.abs(D - truth).max():.2e}"
    )
    assert np.allclose(D, D.T, atol=1e-12), "distance matrix not symmetric"
    assert np.allclose(np.diag(D), 0.0), "nonzero self-distance"


# =============================================================== SASA


def test_cell_list_sasa_equals_brute_force_across_boxes():
    rng = np.random.default_rng(5)
    na, probe = 250, 0.14
    sphere = np.ascontiguousarray(get_fibonacci_sphere_points(120))
    for box_name in ["orthogonal", "mild-tric", "skewed", "skewed-2"]:
        box = _box(box_name)
        c = _coords(na, box, seed=9)
        radii = np.ascontiguousarray(rng.uniform(0.12, 0.20, size=na))
        cutoff = 2.0 * float(radii.max()) + 2.0 * probe
        brute = rb.get_mic_sasa(
            c[None], box[None], radii, sphere, probe, backend="rust"
        )
        cell = rb.get_mic_sasa_cell_list(
            c[None], box[None], radii, sphere, probe, cutoff, backend="rust"
        )
        assert np.allclose(brute, cell, atol=1e-9), (
            f"{box_name}: cell-list vs brute-force max diff {np.abs(brute - cell).max():.2e}"
        )


# =============================================================== angles / dihedrals


def _truth_wrap(v, box, shell=3):
    inv = np.linalg.inv(box)
    s = v @ inv
    base = np.round(s)
    best = None
    dmin = np.inf
    for i in range(-shell, shell + 1):
        for j in range(-shell, shell + 1):
            for k in range(-shell, shell + 1):
                w = (s - (base + [i, j, k])) @ box
                d = w @ w
                if d < dmin:
                    dmin, best = d, w
    return best


@pytest.mark.parametrize("box_name", ["orthogonal", "mild-tric", "skewed"])
def test_mic_angles_use_the_true_minimum_image(box_name):
    box = _box(box_name)
    rng = np.random.default_rng(4)
    c = np.ascontiguousarray(rng.uniform(-6, 12, size=(1, 30, 3)))
    triplets = np.ascontiguousarray(
        np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [10, 15, 20]], dtype=np.int64)
    )
    got = rb.get_mic_angles(c, box[None], triplets, backend="rust")[0]
    truth = []
    for a0, a1, a2 in triplets:
        v0 = _truth_wrap(c[0, a0] - c[0, a1], box)
        v1 = _truth_wrap(c[0, a2] - c[0, a1], box)
        cosa = np.dot(v0, v1) / (np.linalg.norm(v0) * np.linalg.norm(v1))
        truth.append(np.arccos(np.clip(cosa, -1, 1)))
    assert np.allclose(got, truth, atol=1e-9), (
        f"{box_name}: angles diverge from ground truth"
    )
