"""Parity of the Rust long-tail block (geometry, series, topology) against Numba.

Parity splits by data type, for a reason worth stating:

* **integer kernels** (series, topology) -- bit-for-bit. There is no rounding to disagree
  about.
* **floating-point kernels** (centres, radius of gyration, RMSF, flip) -- `TOL`, because
  `lazy_njit` compiles with ``fastmath=True``. These are long accumulation loops, which
  LLVM may vectorise into partial sums, and `flip` has a three-term dot product it may
  contract into FMAs; Rust does neither by default. Divergence measured at 1e-15 relative
  (max 1.1e-14 absolute on `flip`). Verified rather than assumed, as in the `pbc` block:
  Numba fastmath-vs-no-fastmath differs on exactly the same 10/21 centre components that
  Rust does, and Rust matches Numba built with ``fastmath=False`` on 0/21 differences.

That is the same finding as `pbc`, now reaching plain reductions: bit-for-bit parity is
what happens when fastmath has nothing to exploit, not a guarantee the gate can rest on.

Two upstream kernels (`serie_to_chunks`, `occurrence_order_sorted_serie`) read `serie[0]`
before checking the length, so the empty input is an unchecked out-of-bounds read under
`njit`. The Rust ports return empty output; the divergence is tested explicitly rather
than skipped.
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

#: Absorbs the fastmath gap on the floating-point reductions (measured ~1e-15 relative).
TOL = 1e-12


def _close(a, b, what=""):
    assert np.allclose(a, b, rtol=TOL, atol=TOL), f"beyond the fastmath gap {what}"


def _system(n_structures, n_atoms, seed=99):
    rng = np.random.default_rng(seed)
    coordinates = np.ascontiguousarray(rng.uniform(-15.0, 15.0, size=(n_structures, n_atoms, 3)))
    weights = np.ascontiguousarray(rng.uniform(0.5, 16.0, size=n_atoms))
    return coordinates, weights


# ------------------------------------------------------------------ weighted geometry

@pytest.mark.parametrize("ns", [1, 7], ids=["one-structure", "many-structures"])
def test_get_center(ns):
    c, w = _system(ns, 400)
    nb = rb.get_center(c, w, backend="numba")
    rs = rb.get_center(c, w, backend="rust")
    assert rs.shape == (ns, 1, 3), "the singleton axis must survive, it is what broadcasts"
    _close(nb, rs)


def test_get_center_single_structure():
    c, w = _system(1, 400)
    nb = rb.get_center_single_structure(c[0], w, backend="numba")
    rs = rb.get_center_single_structure(c[0], w, backend="rust")
    _close(nb, rs)
    # within one backend the two kernels must agree exactly, not just closely
    assert np.array_equal(rs, rb.get_center(c, w, backend="rust")[0, 0])


@pytest.mark.parametrize("ns", [1, 5], ids=["one-structure", "many-structures"])
def test_get_center_groups_of_atoms(ns):
    groups = np.array([12, 1, 40, 7, 140, 100], dtype=np.int64)
    c, w = _system(ns, int(groups.sum()))
    nb = rb.get_center_groups_of_atoms(c, groups, w, backend="numba")
    rs = rb.get_center_groups_of_atoms(c, groups, w, backend="rust")
    assert rs.shape == (ns, len(groups), 3)
    _close(nb, rs)

    one_nb = rb.get_center_groups_of_atoms_single_structure(c[0], groups, w, backend="numba")
    one_rs = rb.get_center_groups_of_atoms_single_structure(c[0], groups, w, backend="rust")
    _close(one_nb, one_rs)
    assert np.array_equal(one_rs, rs[0]), "same backend, same kernel: must be exact"


def test_a_single_group_reduces_to_the_plain_centre():
    """Cross-check between two independent kernels, not just backend against backend."""
    c, w = _system(3, 200)
    groups = np.array([200], dtype=np.int64)
    grouped = rb.get_center_groups_of_atoms(c, groups, w, backend="rust")
    plain = rb.get_center(c, w, backend="rust")
    assert np.array_equal(grouped[:, 0, :], plain[:, 0, :])


@pytest.mark.parametrize("ns", [1, 4], ids=["one-structure", "many-structures"])
def test_flip(ns):
    c, _ = _system(ns, 300)
    vector = np.array([0.0, 0.6, 0.8])  # unit normal, as the kernel expects
    point = np.array([1.0, -2.0, 0.5])
    nb = rb.flip(c, vector, point, backend="numba")
    rs = rb.flip(c, vector, point, backend="rust")
    _close(nb, rs)

    one_nb = rb.flip_single_structure(c[0], vector, point, backend="numba")
    one_rs = rb.flip_single_structure(c[0], vector, point, backend="rust")
    _close(one_nb, one_rs)
    assert np.array_equal(one_rs, rs[0]), "same backend, same kernel: must be exact"


def test_flipping_twice_restores_the_coordinates():
    c, _ = _system(2, 150)
    vector = np.array([1.0, 0.0, 0.0])
    point = np.array([3.0, 0.0, 0.0])
    once = rb.flip(c, vector, point, backend="rust")
    twice = rb.flip(once, vector, point, backend="rust")
    assert np.allclose(twice, c, atol=1e-12)


@pytest.mark.parametrize("ns", [1, 6], ids=["one-structure", "many-structures"])
def test_get_radius_of_gyration(ns):
    c, w = _system(ns, 500)
    nb = rb.get_radius_of_gyration(c, w, backend="numba")
    rs = rb.get_radius_of_gyration(c, w, backend="rust")
    _close(nb, rs)

    one_nb = rb.get_radius_of_gyration_single_structure(c[0], w, backend="numba")
    one_rs = rb.get_radius_of_gyration_single_structure(c[0], w, backend="rust")
    _close(one_nb, one_rs)
    assert one_rs == rs[0], "same backend, same kernel: must be exact"


@pytest.mark.parametrize("ns", [1, 20], ids=["one-structure", "many-structures"])
def test_get_rmsf(ns):
    c, _ = _system(ns, 250)
    nb = rb.get_rmsf(c, backend="numba")
    rs = rb.get_rmsf(c, backend="rust")
    _close(nb, rs)


def test_rmsf_of_a_single_structure_is_zero():
    c, _ = _system(1, 100)
    assert np.array_equal(rb.get_rmsf(c, backend="rust"), np.zeros(100))


# ------------------------------------------------------------------------- series

SERIES = {
    "consecutive": [0, 1, 2, 3, 4, 5],
    "gapped": [3, 4, 5, 10, 11, 40],
    "singleton": [7],
    "with-repeats": [1, 2, 2, 3, 9],
    "descending-step": [5, 4, 3, 20],
    "negatives": [-8, -7, -6, 0, 1],
}


@pytest.mark.parametrize("name", list(SERIES))
def test_serie_to_chunks_round_trip(name):
    serie = np.array(SERIES[name], dtype=np.int64)
    st_nb, cs_nb = rb.serie_to_chunks(serie, backend="numba")
    st_rs, cs_rs = rb.serie_to_chunks(serie, backend="rust")
    assert np.array_equal(st_nb, st_rs)
    assert np.array_equal(cs_nb, cs_rs)

    back_nb = rb.chunks_to_serie(st_nb, cs_nb, backend="numba")
    back_rs = rb.chunks_to_serie(st_rs, cs_rs, backend="rust")
    assert np.array_equal(back_nb, back_rs)


def test_chunks_round_trip_reproduces_a_consecutive_series():
    serie = np.array([4, 5, 6, 30, 31], dtype=np.int64)
    starts, sizes = rb.serie_to_chunks(serie, backend="rust")
    assert np.array_equal(rb.chunks_to_serie(starts, sizes, backend="rust"), serie)


@pytest.mark.parametrize("name", list(SERIES))
def test_occurrence_order(name):
    serie = np.array(SERIES[name], dtype=np.int64)
    assert np.array_equal(rb.occurrence_order(serie, backend="numba"),
                          rb.occurrence_order(serie, backend="rust"))
    ordered = np.sort(serie)
    assert np.array_equal(rb.occurrence_order_sorted_serie(ordered, backend="numba"),
                          rb.occurrence_order_sorted_serie(ordered, backend="rust"))


def test_the_two_occurrence_orders_agree_on_sorted_input():
    serie = np.array([2, 2, 5, 5, 5, 9], dtype=np.int64)
    assert np.array_equal(rb.occurrence_order(serie, backend="rust"),
                          rb.occurrence_order_sorted_serie(serie, backend="rust"))


def test_empty_series_diverge_because_upstream_reads_out_of_bounds():
    """Upstream indexes `serie[0]` before checking the length; Rust returns empty.

    Asserted rather than skipped so the divergence stays visible. If Numba ever starts
    returning an empty result too, this test fails and the special case can go.
    """
    empty = np.array([], dtype=np.int64)
    starts, sizes = rb.serie_to_chunks(empty, backend="rust")
    assert starts.size == 0 and sizes.size == 0
    assert rb.occurrence_order_sorted_serie(empty, backend="rust").size == 0

    nb_starts, nb_sizes = rb.serie_to_chunks(empty, backend="numba")
    assert nb_starts.size == 1, (
        "upstream no longer produces a phantom chunk for empty input -- drop the special "
        "case in series.rs and assert plain parity")


@pytest.mark.parametrize("item", [
    [[3, 4, 5], [1, 10], [3, 4, 6, 7], [8], [2, 9, 1]],
    [[5, 4, 3]],          # segments are sorted by the kernel
    [[], [1], []],        # empty segments must not break the offsets
])
def test_jit_serialize(item):
    st_nb, va_nb = rb.jit_serialize(item, backend="numba")
    st_rs, va_rs = rb.jit_serialize(item, backend="rust")
    assert np.array_equal(st_nb, st_rs)
    assert np.array_equal(va_nb, va_rs)
    assert len(st_rs) == len(item) + 1, "starts carries a trailing total"
    assert st_rs[-1] == len(va_rs)
    for k, segment in enumerate(item):
        assert list(va_rs[st_rs[k]:st_rs[k + 1]]) == sorted(segment)


# ------------------------------------------------------------------------ topology

BOND_SETS = {
    "chain": ([(0, 1), (1, 2), (2, 3)], 6),
    "two-components": ([(0, 2), (3, 4)], 5),
    "no-bonds": ([], 4),
    "redundant": ([(0, 1), (1, 0), (0, 1)], 3),
    "self-bond": ([(0, 0), (1, 2)], 3),
    "reverse-order": ([(4, 3), (2, 0)], 5),
}


@pytest.mark.parametrize("name", list(BOND_SETS))
def test_get_component_index_from_bonded_atom_pairs(name):
    pairs, n_atoms = BOND_SETS[name]
    arr = np.ascontiguousarray(np.array(pairs, dtype=np.int64).reshape(-1, 2))
    nb = rb.get_component_index_from_bonded_atom_pairs(arr, n_atoms, backend="numba")
    rs = rb.get_component_index_from_bonded_atom_pairs(arr, n_atoms, backend="rust")
    assert np.array_equal(nb, rs), f"{name}: numba {nb} vs rust {rs}"
    # labels must be contiguous from zero -- the property the relabelling pass exists for
    assert set(rs.tolist()) == set(range(rs.max() + 1))


def test_component_labels_follow_first_appearance():
    arr = np.array([[3, 4], [0, 2]], dtype=np.int64)
    rs = rb.get_component_index_from_bonded_atom_pairs(arr, 5, backend="rust")
    assert list(rs) == [0, 1, 0, 2, 2]


def test_a_large_random_bond_graph_agrees():
    rng = np.random.default_rng(5)
    n_atoms = 2000
    arr = np.ascontiguousarray(rng.integers(0, n_atoms, size=(4000, 2)).astype(np.int64))
    nb = rb.get_component_index_from_bonded_atom_pairs(arr, n_atoms, backend="numba")
    rs = rb.get_component_index_from_bonded_atom_pairs(arr, n_atoms, backend="rust")
    assert np.array_equal(nb, rs)


def test_union_and_find_root_mutate_identically():
    """The two helpers are exported separately upstream and mutate their arguments."""
    bonds = [(0, 1), (2, 3), (1, 3), (4, 5)]
    arrays = {}
    for backend in ("numba", "rust"):
        parent = np.arange(8, dtype=np.int64)
        rank = np.zeros(8, dtype=np.int64)
        for a, b in bonds:
            rb_union = getattr(rb, "_union", None)
            if rb_union is None:
                pytest.skip("union helper not exposed through the seam")
            rb_union(parent, rank, a, b, backend=backend)
        roots = [rb._find_root(parent, i, backend=backend) for i in range(8)]
        arrays[backend] = (parent.copy(), rank.copy(), roots)
    assert np.array_equal(arrays["numba"][0], arrays["rust"][0]), "parent trees diverged"
    assert np.array_equal(arrays["numba"][1], arrays["rust"][1]), "ranks diverged"
    assert arrays["numba"][2] == arrays["rust"][2]
