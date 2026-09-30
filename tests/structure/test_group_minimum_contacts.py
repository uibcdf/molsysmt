"""Checking the reusable grouped geometry primitive with analytical reference sets."""

import numpy as np

from molsysmt.structure._group_minimum_contacts import group_minimum_contacts


def test_sparse_groups_use_the_minimum_and_arbitrary_group_indices():
    first = np.array([[0.0, 0, 0], [0.1, 0, 0], [2.0, 0, 0]])
    second = np.array([[0.3, 0, 0], [0.4, 0, 0], [5.0, 0, 0]])
    pairs, distances, images = group_minimum_contacts(
        first, np.array([10, 10, 30]), second, np.array([7, 7, 100]), 0.5
    )
    assert pairs.tolist() == [[10, 7]]
    np.testing.assert_allclose(distances, [0.2])
    assert images.tolist() == [[0, 0, 0]]


def test_no_neighbors_return_typed_empty_group_observations():
    pairs, distances, images = group_minimum_contacts(
        np.array([[0.0, 0, 0]]),
        np.array([10]),
        np.array([[2.0, 0, 0]]),
        np.array([20]),
        0.1,
    )
    assert pairs.shape == (0, 2) and pairs.dtype == np.int64
    assert distances.shape == (0,) and images.shape == (0, 3)


def test_a_periodic_winner_reproduces_the_group_minimum():
    first = np.array([[0.1, 0, 0], [0.12, 0, 0]])
    second = np.array([[0.9, 0, 0], [0.92, 0, 0]])
    pairs, distances, images = group_minimum_contacts(
        first, np.array([4, 4]), second, np.array([9, 9]), 0.3, np.eye(3)
    )
    assert pairs.tolist() == [[4, 9]]
    observed = np.linalg.norm(
        first[:, None] - (second + images[0])[None, :], axis=2
    ).min()
    np.testing.assert_allclose(distances, [0.18])
    np.testing.assert_allclose(distances, [observed])
