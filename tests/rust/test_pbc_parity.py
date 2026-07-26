"""Parity of the Rust `pbc` block against the Numba oracle.

Covers `molsysmt.lib.pbc`: box geometry (lengths, angles, and the box reconstructed from
them), the three wrap kernels and `unwrap`. The four whole-system kernels mutate
`coordinates` in place, so every case runs each backend on its own copy of the same input.

Parity here has three regimes, and conflating them would hide real information:

* **orthogonal boxes** -- bit-for-bit, asserted with `array_equal`.
* **triclinic boxes** -- `ATOL` (1e-12), because `lazy_njit` compiles with
  ``fastmath=True`` and LLVM contracts the fractional wrap's three-term dot products into
  FMAs. Rust does not fuse by default. Verified to be the whole story: rebuilding the same
  kernel with ``fastmath=False`` reproduces Rust bit-for-bit on 2000/2000 vectors. Nothing
  on the Rust side can close this without guessing LLVM's contraction choices.
* **`wrap_to_mic` on triclinic boxes** -- no parity assertion at all. Upstream does not
  return the minimum image there, so this file asserts the *property* instead. See
  `devguide/pending_bugs/wrap_to_mic_triclinic_not_minimum_image.md`.
"""

import numpy as np
import pytest

pytest.importorskip("msm_rust_kernels")

from molsysmt._private import rust_backend as rb  # noqa: E402

ORTHO = np.array([[[6.0, 0.0, 0.0], [0.0, 7.0, 0.0], [0.0, 0.0, 8.0]]])
TRIC = np.array([[[6.0, 0.0, 0.0], [1.5, 6.5, 0.0], [0.8, 1.1, 7.0]]])
BOXES = {"orthogonal": ORTHO, "triclinic": TRIC}

#: Absorbs the fastmath/FMA gap on triclinic boxes; orthogonal cases assert equality.
ATOL = 1e-12


def _agree(kind, a, b, what=""):
    if kind == "orthogonal":
        assert np.array_equal(a, b), f"expected bit-for-bit parity {what}"
    else:
        assert np.allclose(a, b, rtol=0.0, atol=ATOL), f"beyond the fastmath gap {what}"


def _coords(n_structures, n_atoms, spread=25.0, seed=20260724):
    """Coordinates deliberately spilling several box lengths outside the cell."""
    rng = np.random.default_rng(seed)
    return np.ascontiguousarray(
        rng.uniform(-spread, spread, size=(n_structures, n_atoms, 3))
    )


def _boxes(kind, n_structures):
    return np.ascontiguousarray(np.repeat(BOXES[kind], n_structures, axis=0))


# ------------------------------------------------------------------ box geometry


@pytest.mark.parametrize("kind", list(BOXES))
def test_box_is_orthogonal(kind):
    b = _boxes(kind, 4)
    nb = rb.box_is_orthogonal(b, backend="numba")
    rs = rb.box_is_orthogonal(b, backend="rust")
    assert np.array_equal(nb, rs)
    assert bool(nb[0]) is (kind == "orthogonal")
    assert rb.box_is_orthogonal_single_structure(
        b[0], backend="numba"
    ) == rb.box_is_orthogonal_single_structure(b[0], backend="rust")


@pytest.mark.parametrize("kind", list(BOXES))
@pytest.mark.parametrize("fn", ["get_lengths_from_box", "get_angles_from_box"])
def test_lengths_and_angles_from_box(kind, fn):
    b = _boxes(kind, 3)
    nb = getattr(rb, fn)(b, backend="numba")
    rs = getattr(rb, fn)(b, backend="rust")
    _agree(kind, nb, rs)
    one_nb = getattr(rb, fn + "_single_structure")(b[0], backend="numba")
    one_rs = getattr(rb, fn + "_single_structure")(b[0], backend="rust")
    _agree(kind, one_nb, one_rs)


@pytest.mark.parametrize("kind", list(BOXES))
def test_lengths_and_angles_together(kind):
    b = _boxes(kind, 3)
    l_nb, a_nb = rb.get_lengths_and_angles_from_box(b, backend="numba")
    l_rs, a_rs = rb.get_lengths_and_angles_from_box(b, backend="rust")
    _agree(kind, l_nb, l_rs, "(lengths)")
    _agree(kind, a_nb, a_rs, "(angles)")
    # the combined kernel must agree with the two separate ones on its own backend
    assert np.array_equal(l_rs, rb.get_lengths_from_box(b, backend="rust"))
    assert np.array_equal(a_rs, rb.get_angles_from_box(b, backend="rust"))


@pytest.mark.parametrize("kind", list(BOXES))
def test_box_from_lengths_and_angles(kind):
    b = _boxes(kind, 3)
    lengths, angles = rb.get_lengths_and_angles_from_box(b, backend="numba")
    nb = rb.get_box_from_lengths_and_angles(lengths, angles, backend="numba")
    rs = rb.get_box_from_lengths_and_angles(lengths, angles, backend="rust")
    _agree(kind, nb, rs)
    # round trip: reconstructing the box from its own lengths and angles returns it
    assert np.allclose(rs, b, rtol=0.0, atol=1e-12)
    one_nb = rb.get_box_from_lengths_and_angles_single_structure(
        lengths[0], angles[0], backend="numba"
    )
    one_rs = rb.get_box_from_lengths_and_angles_single_structure(
        lengths[0], angles[0], backend="rust"
    )
    _agree(kind, one_nb, one_rs)


# ------------------------------------------------------------------ wrapping


@pytest.mark.parametrize("kind", list(BOXES))
@pytest.mark.parametrize("ns", [1, 4], ids=["one-structure", "many-structures"])
@pytest.mark.parametrize("fn", ["wrap_to_pbc", "wrap_to_pbc_center", "wrap_to_mic"])
def test_wrap_kernels_mutate_identically(kind, ns, fn):
    b = _boxes(kind, ns)
    origin = np.zeros(3)
    c_nb, c_rs = _coords(ns, 200), _coords(ns, 200)
    assert np.array_equal(c_nb, c_rs), "the two copies must start identical"

    assert getattr(rb, fn)(c_nb, b, origin, backend="numba") is None
    assert getattr(rb, fn)(c_rs, b, origin, backend="rust") is None
    if fn == "wrap_to_mic" and kind == "triclinic":
        pytest.skip("upstream is not minimum-image here; see test_wrap_to_mic_*")
    _agree(kind, c_nb, c_rs)


@pytest.mark.parametrize("kind", list(BOXES))
def test_wrap_respects_a_non_zero_origin(kind):
    b = _boxes(kind, 2)
    origin = np.array([-3.0, 1.25, 0.5])
    c_nb, c_rs = _coords(2, 150), _coords(2, 150)
    rb.wrap_to_pbc(c_nb, b, origin, backend="numba")
    rb.wrap_to_pbc(c_rs, b, origin, backend="rust")
    _agree(kind, c_nb, c_rs)


@pytest.mark.parametrize("kind", list(BOXES))
@pytest.mark.parametrize(
    "fn",
    [
        "wrap_to_pbc_vector_single_structure",
        "wrap_to_pbc_center_vector_single_structure",
        "wrap_to_mic_vector_single_structure",
    ],
)
def test_wrap_vector_helpers(kind, fn):
    if fn == "wrap_to_mic_vector_single_structure" and kind == "triclinic":
        pytest.skip("upstream is not minimum-image here; see test_wrap_to_mic_*")
    b = _boxes(kind, 1)[0]
    rng = np.random.default_rng(7)
    for _ in range(50):
        v = np.ascontiguousarray(rng.uniform(-30.0, 30.0, size=3))
        nb = getattr(rb, fn)(v.copy(), b, backend="numba")
        rs = getattr(rb, fn)(v.copy(), b, backend="rust")
        _agree(kind, nb, rs, f"for {v}: numba {nb} vs rust {rs}")


def _is_minimum_image(w, b):
    n = np.linalg.norm(w)
    return all(
        np.linalg.norm(w + i * b[0] + j * b[1] + k * b[2]) >= n - 1e-12
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        for k in (-1, 0, 1)
    )


def test_wrap_to_mic_is_minimum_image_on_a_triclinic_box():
    """The deliberate correction: Rust returns the minimum image, upstream mostly does not.

    Upstream searches the 27 images of the *original* vector, so when the input sits
    several box lengths outside the cell none of the candidates is near the origin and the
    [0,1) fractional wrap wins by default -- which is the primitive cell, not the minimum
    image. Rust searches around the wrapped candidate, as `unwrap.py` already does.
    """
    b = TRIC[0]
    rng = np.random.default_rng(11)
    vectors = [
        np.ascontiguousarray(rng.uniform(-20.0, 20.0, size=3)) for _ in range(200)
    ]

    rust_ok = sum(
        _is_minimum_image(
            rb.wrap_to_mic_vector_single_structure(v.copy(), b, backend="rust"), b
        )
        for v in vectors
    )
    assert rust_ok == len(vectors), f"Rust must always be minimum-image, got {rust_ok}"

    numba_ok = sum(
        _is_minimum_image(
            rb.wrap_to_mic_vector_single_structure(v.copy(), b, backend="numba"), b
        )
        for v in vectors
    )
    assert numba_ok < len(vectors), (
        "upstream now returns the minimum image on triclinic boxes -- the bug this "
        "divergence works around has been fixed, so drop the correction in pbc.rs and "
        "restore plain parity"
    )


def test_wrap_to_mic_is_minimum_image_on_an_orthogonal_box_on_both_backends():
    """The orthogonal branch was always correct; the defect is triclinic-only."""
    b = ORTHO[0]
    rng = np.random.default_rng(13)
    for _ in range(100):
        v = np.ascontiguousarray(rng.uniform(-25.0, 25.0, size=3))
        for backend in ("numba", "rust"):
            w = rb.wrap_to_mic_vector_single_structure(v.copy(), b, backend=backend)
            assert _is_minimum_image(w, b), f"{backend} failed on {v}"


# ------------------------------------------------------------------ unwrap


@pytest.mark.parametrize("kind", list(BOXES))
def test_unwrap_makes_trajectories_continuous_identically(kind):
    b = _boxes(kind, 6)
    c_nb, c_rs = _coords(6, 120, spread=8.0), _coords(6, 120, spread=8.0)
    assert rb.unwrap(c_nb, b, backend="numba") is None
    assert rb.unwrap(c_rs, b, backend="rust") is None
    _agree(kind, c_nb, c_rs)


def test_unwrap_agrees_on_exact_half_box_jumps():
    """`unwrap` rounds half to even (Python semantics); `f64::round` would not.

    A displacement of exactly half a box length is the input that separates the two
    rounding modes, and getting it wrong moves an atom by a whole box length.
    """
    b = np.ascontiguousarray(np.repeat(ORTHO, 3, axis=0))
    lengths = np.array([6.0, 7.0, 8.0])
    base = np.zeros((3, 4, 3))
    for s in range(1, 3):
        # every atom jumps by exactly +/- L/2 between consecutive structures
        base[s] = (
            base[s - 1]
            + np.array(
                [
                    [0.5, -0.5, 1.5],
                    [-1.5, 2.5, -2.5],
                    [0.5, 0.5, 0.5],
                    [-0.5, -0.5, -0.5],
                ]
            )
            * lengths
        )
    c_nb, c_rs = np.ascontiguousarray(base.copy()), np.ascontiguousarray(base.copy())
    rb.unwrap(c_nb, b, backend="numba")
    rb.unwrap(c_rs, b, backend="rust")
    assert np.array_equal(c_nb, c_rs), (
        f"rounding-mode divergence on exact ties:\n{c_nb}\nvs\n{c_rs}"
    )
