"""Parity of the Rust principal-axes block against the Numba oracle.

Eigenvectors are defined only up to sign, so this file cannot compare them element by
element. It asserts instead:

* **eigenvalues** agree within tolerance -- those are unambiguous, and returned ascending;
* **eigenvectors agree up to sign**, i.e. `|v_rust . v_numba| == 1`;
* the **defining property** `M v = lambda v`, orthonormality, and the physical ordering.

The last group is the point: it would catch a wrong axis that both backends happened to
share, which a parity assertion never can.

The Rust port additionally fixes the sign deterministically (largest-magnitude component
positive) so that switching backend cannot flip an axis. Upstream leaves it to LAPACK; see
`devguide/pending_bugs/principal_axes_eigenvector_sign_unspecified.md`.
"""

import numpy as np
import pytest

import molsysmt._rust  # noqa: F401, E402

from molsysmt._private import rust_backend as rb  # noqa: E402

TOL = 1e-9
KERNELS = ["get_principal_inertia_axes", "get_principal_geometric_axes"]


def _system(n_structures, n_atoms, seed=77):
    rng = np.random.default_rng(seed)
    c = np.ascontiguousarray(rng.uniform(-12.0, 12.0, size=(n_structures, n_atoms, 3)))
    w = np.ascontiguousarray(rng.uniform(1.0, 32.0, size=n_atoms))
    return c, w


def _assert_axes_match(nb_axes, rs_axes):
    """Row-wise agreement up to sign."""
    for i in range(3):
        dot = float(np.dot(nb_axes[i], rs_axes[i]))
        assert abs(abs(dot) - 1.0) < 1e-7, (
            f"axis {i} is not parallel between backends (|cos| = {abs(dot)})"
        )


@pytest.mark.parametrize("fn", KERNELS)
@pytest.mark.parametrize("ns", [1, 5], ids=["one-structure", "many-structures"])
def test_axes_parity(fn, ns):
    c, w = _system(ns, 300)
    nb_values, nb_axes = getattr(rb, fn)(c, w, backend="numba")
    rs_values, rs_axes = getattr(rb, fn)(c, w, backend="rust")
    assert rs_values.shape == (ns, 3) and rs_axes.shape == (ns, 3, 3)
    assert np.allclose(nb_values, rs_values, rtol=TOL, atol=TOL), "eigenvalues diverged"
    for s in range(ns):
        _assert_axes_match(nb_axes[s], rs_axes[s])


@pytest.mark.parametrize("fn", KERNELS)
def test_axes_parity_single_structure(fn):
    c, w = _system(1, 300)
    nb_values, nb_axes = getattr(rb, fn + "_single_structure")(c[0], w, backend="numba")
    rs_values, rs_axes = getattr(rb, fn + "_single_structure")(c[0], w, backend="rust")
    assert rs_axes.shape == (3, 3)
    assert np.allclose(nb_values, rs_values, rtol=TOL, atol=TOL)
    _assert_axes_match(nb_axes, rs_axes)


@pytest.mark.parametrize("fn", KERNELS)
def test_eigenvalues_are_ascending_and_axes_orthonormal(fn):
    c, w = _system(4, 250)
    values, axes = getattr(rb, fn)(c, w, backend="rust")
    for s in range(4):
        assert np.all(np.diff(values[s]) >= -1e-12), f"not ascending: {values[s]}"
        assert np.allclose(axes[s] @ axes[s].T, np.eye(3), rtol=0.0, atol=1e-10), (
            "not orthonormal"
        )


def test_axes_satisfy_the_eigenvalue_equation():
    """Rebuilds the inertia tensor independently and checks M v = lambda v."""
    c, w = _system(1, 200)
    values, axes = rb.get_principal_inertia_axes_single_structure(
        c[0], w, backend="rust"
    )

    centre = np.average(c[0], axis=0, weights=w)
    d = c[0] - centre
    m = np.zeros((3, 3))
    m[0, 0] = np.sum(w * (d[:, 1] ** 2 + d[:, 2] ** 2))
    m[1, 1] = np.sum(w * (d[:, 0] ** 2 + d[:, 2] ** 2))
    m[2, 2] = np.sum(w * (d[:, 0] ** 2 + d[:, 1] ** 2))
    m[0, 1] = m[1, 0] = -np.sum(w * d[:, 0] * d[:, 1])
    m[0, 2] = m[2, 0] = -np.sum(w * d[:, 0] * d[:, 2])
    m[1, 2] = m[2, 1] = -np.sum(w * d[:, 1] * d[:, 2])

    for i in range(3):
        assert np.allclose(m @ axes[i], values[i] * axes[i], rtol=0.0, atol=1e-6), (
            f"axis {i}"
        )


def test_a_rod_puts_its_smallest_inertia_along_itself():
    """Physical check, independent of both backends' numerics."""
    n = 21
    c = np.zeros((1, n, 3))
    c[0, :, 0] = np.linspace(-5.0, 5.0, n)
    w = np.ones(n)
    values, axes = rb.get_principal_inertia_axes(c, w, backend="rust")
    assert values[0, 0] < 1e-9, "inertia about the rod axis should vanish"
    assert abs(abs(axes[0, 0, 0]) - 1.0) < 1e-9, f"expected x, got {axes[0, 0]}"


def test_the_rust_sign_convention_is_stable():
    """Same input, same signs -- and the leading component is always positive."""
    c, w = _system(3, 200)
    _, first = rb.get_principal_geometric_axes(c, w, backend="rust")
    _, second = rb.get_principal_geometric_axes(c, w, backend="rust")
    assert np.array_equal(first, second)
    for s in range(3):
        for i in range(3):
            lead = int(np.argmax(np.abs(first[s, i])))
            assert first[s, i, lead] > 0.0, (
                f"structure {s} axis {i} not sign-normalised"
            )
