"""Analytic truth tests for distance reductions and neighborhood relations."""

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def _structures(coordinates):
    coordinates = np.asarray(coordinates, dtype=np.float64)
    return Structures(coordinates=coordinates * msm.pyunitwizard.unit("nm"))


def _values(quantity):
    return msm.pyunitwizard.get_value(quantity, to_unit="nm")


def test_minimum_distance_selects_the_closed_form_pair(float64_kernel_atol):
    """Select distance 1 from an explicit two-by-two Cartesian matrix."""

    system = _structures([[[0.0, 0.0, 0.0], [4.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 3.0, 0.0]]])
    pairs, distances = msm.structure.get_minimum_distances(
        system,
        selection=[0, 1],
        selection_2=[2, 3],
        pbc=False,
    )

    np.testing.assert_array_equal(pairs, np.array([[0, 0]]))
    np.testing.assert_allclose(
        _values(distances), np.array([1.0]), rtol=0.0, atol=float64_kernel_atol
    )


def test_maximum_distance_selects_the_closed_form_pair(float64_kernel_atol):
    """Select distance 5 from an explicit two-by-two Cartesian matrix."""

    system = _structures([[[0.0, 0.0, 0.0], [4.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 3.0, 0.0]]])
    pairs, distances = msm.structure.get_maximum_distances(
        system,
        selection=[0, 1],
        selection_2=[2, 3],
        pbc=False,
    )

    np.testing.assert_array_equal(pairs, np.array([[1, 1]]))
    np.testing.assert_allclose(
        _values(distances), np.array([5.0]), rtol=0.0, atol=float64_kernel_atol
    )


def test_contacts_apply_an_inclusive_exact_cutoff():
    """Classify a two-by-two distance matrix at an inclusive 3 nm threshold."""

    system = _structures([[[0.0, 0.0, 0.0], [4.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 3.0, 0.0]]])
    observed = msm.structure.get_contacts(
        system,
        selection=[0, 1],
        selection_2=[2, 3],
        threshold="3 nm",
        pbc=False,
        cell_list=False,
        use_gpu=False,
    )
    expected = np.array([[[True, True], [True, False]]])

    np.testing.assert_array_equal(observed, expected)


def test_neighbors_are_sorted_by_closed_form_distance(float64_kernel_atol):
    """Return the two nearest non-self indices for four collinear points."""

    system = _structures(
        [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [3.0, 0.0, 0.0], [10.0, 0.0, 0.0]]]
    )
    neighbors, distances = msm.structure.get_neighbors(
        system,
        selection="all",
        n_neighbors=2,
        pbc=False,
    )
    expected_neighbors = np.array([[[1, 2], [0, 2], [1, 0], [2, 1]]])
    expected_distances = np.array([[[1.0, 3.0], [1.0, 2.0], [2.0, 3.0], [7.0, 9.0]]])

    np.testing.assert_array_equal(neighbors, expected_neighbors)
    np.testing.assert_allclose(
        _values(distances),
        expected_distances,
        rtol=0.0,
        atol=float64_kernel_atol,
    )
