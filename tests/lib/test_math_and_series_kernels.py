import numpy as np

from molsysmt.lib.math import (
    angle,
    cross_product,
    dihedral_angle,
    dot_product,
    inverse_matrix_3x3,
    matmul,
    minimum_distance_between_coordinate_sets,
    minimum_distance_masked_not_bonded,
    norm_vector,
    normalize_vector,
    quaternion_to_rotation_matrix,
    rodrigues_rotation,
    transpmatmul,
)
from molsysmt.lib.series import (
    chunks_to_serie,
    occurrence_order,
    occurrence_order_sorted_serie,
    serie_to_chunks,
    serialized_lists,
)


def test_math_primitives_cover_vector_and_matrix_helpers():
    lower = np.array([[2.0, 0.0, 0.0], [3.0, 4.0, 0.0], [5.0, 6.0, 8.0]], dtype=np.float64)
    inv = inverse_matrix_3x3(lower)
    np.testing.assert_allclose(inv @ lower, np.eye(3), atol=1e-12)

    vector = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    np.testing.assert_allclose(matmul(lower, vector), lower @ vector)
    np.testing.assert_allclose(transpmatmul(lower, vector), lower.T @ vector)

    other = np.array([3.0, -2.0, 1.0], dtype=np.float64)
    assert np.isclose(dot_product(vector, other), np.dot(vector, other))
    np.testing.assert_allclose(cross_product(vector, other), np.cross(vector, other))
    assert np.isclose(norm_vector(vector), np.linalg.norm(vector))
    np.testing.assert_allclose(normalize_vector(vector), vector / np.linalg.norm(vector))


def test_angle_dihedral_rotation_and_quaternion_helpers():
    vect0 = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    vect1 = np.array([0.0, 1.0, 0.0], dtype=np.float64)
    vect2 = np.array([0.0, 0.0, 1.0], dtype=np.float64)

    assert np.isclose(angle(vect0, vect1), np.pi / 2)
    assert np.isclose(dihedral_angle(vect0, vect1, vect2), np.pi / 2)

    rotated = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    rodrigues_rotation(rotated, np.array([0.0, 0.0, 1.0], dtype=np.float64), np.pi / 2)
    np.testing.assert_allclose(rotated, np.array([0.0, 1.0, 0.0]), atol=1e-12)

    q = np.array([np.cos(np.pi / 4), 0.0, 0.0, np.sin(np.pi / 4)], dtype=np.float64)
    rotation = quaternion_to_rotation_matrix(q)
    np.testing.assert_allclose(rotation @ np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), atol=1e-12)


def test_minimum_distance_helpers_cover_masked_and_candidate_paths():
    coordinates = np.array(
        [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [0.0, 4.0, 0.0]], dtype=np.float64
    )
    include_mask = np.array([1, 1, 1], dtype=np.uint8)
    bonded_matrix = np.zeros((3, 3), dtype=np.uint8)
    bonded_matrix[0, 1] = bonded_matrix[1, 0] = 1
    assert np.isclose(minimum_distance_masked_not_bonded(coordinates, include_mask, bonded_matrix), 4.0)

    existing = np.array([[0.0, 0.0, 0.0], [4.0, 0.0, 0.0]], dtype=np.float64)
    candidate = np.array([[0.0, 3.0, 0.0], [10.0, 0.0, 0.0]], dtype=np.float64)
    existing_mask = np.array([1, 1], dtype=np.uint8)
    candidate_mask = np.array([1, 1], dtype=np.uint8)
    bonded = np.zeros((2, 4), dtype=np.uint8)
    assert np.isclose(
        minimum_distance_between_coordinate_sets(
            existing,
            existing_mask,
            candidate,
            candidate_mask,
            2,
            bonded,
        ),
        3.0,
    )


def test_series_helpers_cover_chunk_and_occurrence_paths():
    serie = np.array([1, 2, 3, 7, 8, 10], dtype=np.int64)
    starts, sizes = serie_to_chunks(serie)
    np.testing.assert_array_equal(starts, np.array([1, 7, 10], dtype=np.int64))
    np.testing.assert_array_equal(sizes, np.array([3, 2, 1], dtype=np.int64))
    np.testing.assert_array_equal(chunks_to_serie(starts, sizes), serie)

    np.testing.assert_array_equal(
        occurrence_order(np.array([9, 4, 9, 7, 4], dtype=np.int64)),
        np.array([0, 1, 0, 2, 1], dtype=np.int64),
    )
    np.testing.assert_array_equal(
        occurrence_order_sorted_serie(np.array([1, 1, 2, 2, 4], dtype=np.int64)),
        np.array([0, 0, 1, 1, 2], dtype=np.int64),
    )

    serialized_from_list = serialized_lists([[3, 4, 5], [1, 10], [8]])
    np.testing.assert_array_equal(serialized_from_list.indices, np.array([0, 1, 2], dtype=np.int64))
    np.testing.assert_array_equal(serialized_from_list.starts, np.array([0, 3, 5, 6], dtype=np.int64))

    serialized_from_dict = serialized_lists({7: [1, 10], 2: [3, 4, 5], 8: [8]})
    np.testing.assert_array_equal(serialized_from_dict.indices, np.array([2, 7, 8], dtype=np.int64))
    np.testing.assert_array_equal(serialized_from_dict.starts, np.array([0, 3, 5, 6], dtype=np.int64))
