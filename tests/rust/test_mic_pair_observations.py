"""Check observed pair images against an independent lattice search."""

import itertools

import numpy as np
import pytest

from molsysmt._private.rust_backend import (
    get_mic_distances_pairs_single_structure,
    get_mic_pair_observations,
)


def _minimum_distance(raw, box):
    base = np.rint(-raw @ np.linalg.inv(box)).astype(int)
    return min(
        np.linalg.norm(raw + (base + offset) @ box)
        for offset in itertools.product(range(-3, 4), repeat=3)
    )


def test_pair_images_add_to_second_coordinate_in_original_box_basis():
    diagonal = 2**-0.5
    boxes = np.asarray([
        np.diag([1.0, 1.2, 1.4]),
        [[1.0, 0.0, 0.0], [0.48, 1.0, 0.0], [0.45, 0.43, 1.0]],
        [[diagonal, diagonal, 0.0], [-diagonal, diagonal, 0.0], [0.0, 0.0, 1.0]],
    ])
    first = np.asarray([
        [0.95, 0.00, 0.00],
        [0.10, 0.10, 0.10],
        [0.94, 0.85, 0.70],
        [2.50, -1.60, 0.33],
        [0.15, 0.25, -0.10],
        [-0.90, 1.15, 0.45],
        [0.0, 0.0, 0.0],
    ])
    second = np.asarray([
        [0.05, 0.00, 0.00],
        [0.20, 0.15, 0.10],
        [0.08, 0.10, 0.05],
        [-0.24, 1.72, -0.48],
        [0.80, 0.65, 0.35],
        [1.30, -0.35, 0.75],
        [-1.65, -1.05, 1.20],
    ])
    frames = np.asarray([0, 0, 1, 1, 2, 2, 2], dtype=np.int64)

    distances, images = get_mic_pair_observations(first, second, boxes, frames)
    assert distances.shape == (7,)
    assert images.shape == (7, 3)
    assert images.dtype == np.int32
    np.testing.assert_array_equal(images[0], [1, 0, 0])
    np.testing.assert_array_equal(images[1], [0, 0, 0])
    np.testing.assert_array_equal(images[6], [2, 0, -1])

    for index, frame in enumerate(frames):
        raw = second[index] - first[index]
        observed = raw + images[index] @ boxes[frame]
        np.testing.assert_allclose(np.linalg.norm(observed), distances[index], atol=1e-12)
        np.testing.assert_allclose(
            distances[index], _minimum_distance(raw, boxes[frame]), atol=1e-12
        )

    repeated = get_mic_pair_observations(first, second, boxes, frames)
    np.testing.assert_array_equal(repeated[1], images)


def test_pair_image_rejects_invalid_frame_index():
    first = np.zeros((1, 3))
    with pytest.raises(ValueError, match="outside the box axis"):
        get_mic_pair_observations(first, first, np.eye(3)[None], [1])


def test_rotated_orthogonal_box_uses_lattice_distance_in_existing_kernel():
    diagonal = 2**-0.5
    box = np.asarray([
        [diagonal, diagonal, 0.0],
        [-diagonal, diagonal, 0.0],
        [0.0, 0.0, 1.0],
    ])
    raw = np.asarray([[-1.65, -1.05, 1.20]])
    distance = get_mic_distances_pairs_single_structure(
        np.zeros_like(raw), raw, box
    )[0]
    np.testing.assert_allclose(distance, _minimum_distance(raw[0], box), atol=1e-12)
