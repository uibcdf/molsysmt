import numpy as np

from molsysmt.lib.pbc.get_angles_from_box import get_angles_from_box, get_angles_from_box_single_structure
from molsysmt.lib.pbc.get_box_from_lengths_and_angles import get_box_from_lengths_and_angles_single_structure
from molsysmt.lib.pbc.get_lengths_from_box import get_lengths_from_box, get_lengths_from_box_single_structure
from molsysmt.lib.pbc.unwrap import unwrap
from molsysmt.lib.structure.get_mic_angles import get_mic_angles, get_mic_angles_single_structure
from molsysmt.lib.structure.get_mic_dihedral_angles import (
    get_mic_dihedral_angles,
    get_mic_dihedral_angles_single_structure,
)
from molsysmt.lib.structure.get_mic_distances import (
    get_mic_distance_two_points_single_structure,
    get_mic_distances,
    get_mic_distances_pairs,
    get_mic_distances_single_system,
    get_mic_distances_single_system_single_structure,
)
from molsysmt.lib.structure.set_mic_dihedral_angles import (
    set_mic_dihedral_angles,
    set_mic_dihedral_angles_single_structure,
)
from molsysmt.lib.structure.shift_mic_dihedral_angles import (
    shift_mic_dihedral_angles,
    shift_mic_dihedral_angles_single_structure,
)


def _triclinic_box():
    return get_box_from_lengths_and_angles_single_structure(
        np.array([2.0, 3.0, 4.0], dtype=np.float64),
        np.array([np.pi / 2, np.pi / 2, 2.0 * np.pi / 3], dtype=np.float64),
    )


def test_lengths_and_angles_helpers_and_unwrap_cover_triclinic_paths():
    box = _triclinic_box()
    lengths = get_lengths_from_box_single_structure(box)
    angles = get_angles_from_box_single_structure(box)
    np.testing.assert_allclose(lengths, np.array([2.0, 3.0, 4.0]), atol=1e-12)
    np.testing.assert_allclose(angles, np.array([np.pi / 2, np.pi / 2, 2.0 * np.pi / 3]), atol=1e-12)

    batch = box[np.newaxis, :, :]
    np.testing.assert_allclose(get_lengths_from_box(batch)[0], lengths)
    np.testing.assert_allclose(get_angles_from_box(batch)[0], angles)

    coordinates = np.array(
        [
            [[0.1, 0.1, 0.1], [0.2, 0.2, 0.2]],
            [[2.2, 0.2, 0.2], [0.3, 3.3, 0.3]],
            [[4.1, 0.4, 0.4], [0.5, 6.1, 0.5]],
        ],
        dtype=np.float64,
    )
    unwrap(coordinates, np.repeat(batch, 3, axis=0))
    assert coordinates.shape == (3, 2, 3)
    assert np.all(np.isfinite(coordinates))


def test_mic_distance_angle_and_dihedral_kernels_cover_single_and_batch_paths():
    box = _triclinic_box()
    coordinates = np.array(
        [[0.1, 0.1, 0.1], [1.8, 0.2, 0.1], [0.2, 2.8, 0.1], [0.2, 2.7, 3.6]],
        dtype=np.float64,
    )

    single_system = get_mic_distances_single_system_single_structure(coordinates, box)
    assert single_system.shape == (4, 4)
    assert np.allclose(single_system, single_system.T)

    point_distance = get_mic_distance_two_points_single_structure(coordinates[0], coordinates[1], box, None, None)
    assert np.isfinite(point_distance)

    batch_coordinates = coordinates[np.newaxis, :, :]
    batch_box = box[np.newaxis, :, :]
    assert get_mic_distances_single_system(batch_coordinates, batch_box).shape == (1, 4, 4)
    assert get_mic_distances(batch_coordinates, batch_coordinates, batch_box).shape == (1, 4, 4)
    assert get_mic_distances_pairs(batch_coordinates, batch_coordinates, batch_box).shape == (1, 4)

    triplets = np.array([[0, 1, 2]], dtype=np.int64)
    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    assert get_mic_angles_single_structure(coordinates, box, triplets).shape == (1,)
    assert get_mic_angles(batch_coordinates, batch_box, triplets).shape == (1, 1)
    assert get_mic_dihedral_angles_single_structure(coordinates, box, quartets).shape == (1,)
    assert get_mic_dihedral_angles(batch_coordinates, batch_box, quartets).shape == (1, 1)


def test_mic_dihedral_set_and_shift_kernels_cover_single_and_batch_paths():
    box = np.eye(3, dtype=np.float64) * 10.0
    coordinates = np.array(
        [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 1.0]],
        dtype=np.float64,
    )
    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    blocks = np.array([[False, False, False, True]], dtype=np.bool_)

    target = np.array([np.pi / 2], dtype=np.float64)
    coords_single = coordinates.copy()
    set_mic_dihedral_angles_single_structure(coords_single, box, target, quartets, blocks)
    np.testing.assert_allclose(
        get_mic_dihedral_angles_single_structure(coords_single, box, quartets),
        target,
        atol=1e-12,
    )

    coords_shifted = coords_single.copy()
    shift_mic_dihedral_angles_single_structure(
        coords_shifted,
        box,
        np.array([-np.pi / 2], dtype=np.float64),
        quartets,
        blocks,
    )
    np.testing.assert_allclose(
        get_mic_dihedral_angles_single_structure(coords_shifted, box, quartets),
        np.array([0.0], dtype=np.float64),
        atol=1e-12,
    )

    batch_coordinates = coordinates[np.newaxis, :, :].copy()
    batch_box = box[np.newaxis, :, :]
    set_mic_dihedral_angles(batch_coordinates, batch_box, target[np.newaxis, :], quartets, blocks)
    np.testing.assert_allclose(
        get_mic_dihedral_angles_single_structure(batch_coordinates[0], box, quartets),
        target,
        atol=1e-12,
    )

    shift_mic_dihedral_angles(
        batch_coordinates,
        batch_box,
        np.array([[-np.pi / 2]], dtype=np.float64),
        quartets,
        blocks,
        np.array([0], dtype=np.int64),
    )
    np.testing.assert_allclose(
        get_mic_dihedral_angles_single_structure(batch_coordinates[0], box, quartets),
        np.array([0.0], dtype=np.float64),
        atol=1e-12,
    )
