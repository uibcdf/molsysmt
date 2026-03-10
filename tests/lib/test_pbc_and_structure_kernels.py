import numpy as np

from molsysmt.lib.pbc.box_is_orthogonal import (
    box_is_orthogonal,
    box_is_orthogonal_single_structure,
)
from molsysmt.lib.pbc.get_box_from_lengths_and_angles import (
    get_box_from_lengths_and_angles,
    get_box_from_lengths_and_angles_single_structure,
)
from molsysmt.lib.pbc.get_lengths_and_angles_from_box import (
    get_lengths_and_angles_from_box,
    get_lengths_and_angles_from_box_single_structure,
)
from molsysmt.lib.pbc.wrap_to_mic import (
    wrap_to_mic,
    wrap_to_mic_vector_single_structure,
)
from molsysmt.lib.pbc.wrap_to_pbc import (
    wrap_to_pbc,
    wrap_to_pbc_center,
    wrap_to_pbc_center_vector_single_structure,
    wrap_to_pbc_vector_single_structure,
)
from molsysmt.lib.structure.get_angles import get_angles, get_angles_single_structure
from molsysmt.lib.structure.get_dihedral_angles import (
    get_dihedral_angles,
    get_dihedral_angles_single_structure,
)
from molsysmt.lib.structure.get_distances import (
    get_distance_two_points_single_structure,
    get_distances,
    get_distances_pairs,
    get_distances_pairs_single_structure,
    get_distances_single_structure,
    get_distances_single_system,
    get_distances_single_system_single_structure,
)
from molsysmt.lib.structure.get_least_rmsd import (
    get_least_rmsd,
    get_least_rmsd_single_structure,
    get_least_rmsd_with_single_reference_structure,
)
from molsysmt.lib.structure.get_rmsd import (
    get_rmsd,
    get_rmsd_single_structure,
    get_rmsd_with_single_reference_structure,
)
from molsysmt.lib.topology.get_component_index_from_bonded_atom_pairs import (
    get_component_index_from_bonded_atom_pairs,
)


def test_box_roundtrip_and_orthogonality_kernels():
    lengths = np.array([2.0, 3.0, 4.0], dtype=np.float64)
    angles = np.array([np.pi / 2, np.pi / 2, np.pi / 2], dtype=np.float64)

    box = get_box_from_lengths_and_angles_single_structure(lengths, angles)
    out_lengths, out_angles = get_lengths_and_angles_from_box_single_structure(box)
    assert box_is_orthogonal_single_structure(box) is True
    np.testing.assert_allclose(out_lengths, lengths)
    np.testing.assert_allclose(out_angles, angles)

    batch_box = get_box_from_lengths_and_angles(lengths[np.newaxis, :], angles[np.newaxis, :])
    batch_lengths, batch_angles = get_lengths_and_angles_from_box(batch_box)
    np.testing.assert_allclose(batch_lengths[0], lengths)
    np.testing.assert_allclose(batch_angles[0], angles)
    np.testing.assert_array_equal(box_is_orthogonal(batch_box), np.array([True]))


def test_wrap_kernels_for_orthogonal_box():
    box = np.eye(3, dtype=np.float64) * 10.0
    vector = np.array([11.2, -0.1, 5.5], dtype=np.float64)

    wrapped_pbc = wrap_to_pbc_vector_single_structure(vector, box, None, None)
    np.testing.assert_allclose(wrapped_pbc, np.array([1.2, 9.9, 5.5]))

    wrapped_center = wrap_to_pbc_center_vector_single_structure(vector, box, None, None)
    np.testing.assert_allclose(wrapped_center, np.array([1.2, -0.1, -4.5]))

    wrapped_mic = wrap_to_mic_vector_single_structure(vector, box, None, None)
    np.testing.assert_allclose(wrapped_mic, np.array([1.2, -0.1, -4.5]))

    coordinates = np.array([[[11.2, -0.1, 5.5], [-1.0, 10.1, 10.0]]], dtype=np.float64)
    wrap_to_pbc(coordinates, box[np.newaxis, :, :], np.zeros(3, dtype=np.float64))
    np.testing.assert_allclose(coordinates[0, 0], np.array([1.2, 9.9, 5.5]))
    np.testing.assert_allclose(coordinates[0, 1], np.array([9.0, 0.1, 0.0]))

    coordinates = np.array([[[11.2, -0.1, 5.5], [-1.0, 10.1, 10.0]]], dtype=np.float64)
    wrap_to_pbc_center(coordinates, box[np.newaxis, :, :], np.zeros(3, dtype=np.float64))
    np.testing.assert_allclose(coordinates[0, 0], np.array([1.2, -0.1, -4.5]))

    coordinates = np.array([[[11.2, -0.1, 5.5], [-1.0, 10.1, 10.0]]], dtype=np.float64)
    wrap_to_mic(coordinates, box[np.newaxis, :, :], np.zeros(3, dtype=np.float64))
    np.testing.assert_allclose(coordinates[0, 0], np.array([1.2, -0.1, -4.5]))


def test_distance_kernels_cover_single_and_batched_paths():
    p0 = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    p1 = np.array([3.0, 4.0, 0.0], dtype=np.float64)
    assert np.isclose(get_distance_two_points_single_structure(p0, p1), 5.0)

    coords = np.array([[[0.0, 0.0, 0.0], [3.0, 4.0, 0.0]]], dtype=np.float64)
    distances = get_distances_single_system(coords)
    np.testing.assert_allclose(distances[0, 0, 1], 5.0)
    np.testing.assert_allclose(get_distances_single_system_single_structure(coords[0]), np.array([[0.0, 5.0], [5.0, 0.0]]))

    coords2 = np.array([[[0.0, 0.0, 0.0], [0.0, 0.0, 12.0]]], dtype=np.float64)
    pair = get_distances_pairs(coords, coords2)
    np.testing.assert_allclose(pair[0], np.array([0.0, 13.0]))
    np.testing.assert_allclose(get_distances_pairs_single_structure(coords[0], coords2[0]), np.array([0.0, 13.0]))

    mixed = get_distances(coords, coords2)
    assert mixed.shape == (1, 2, 2)


def test_angle_and_dihedral_kernels():
    coordinates = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0],
        ],
        dtype=np.float64,
    )
    triplets = np.array([[0, 1, 2]], dtype=np.int64)
    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)

    angle = get_angles_single_structure(coordinates, triplets)
    np.testing.assert_allclose(angle, np.array([np.pi / 2]))
    np.testing.assert_allclose(get_angles(coordinates[np.newaxis, :, :], triplets), np.array([[np.pi / 2]]))

    dihedral = get_dihedral_angles_single_structure(coordinates, quartets)
    np.testing.assert_allclose(dihedral, np.array([-np.pi / 2]))
    np.testing.assert_allclose(get_dihedral_angles(coordinates[np.newaxis, :, :], quartets), np.array([[-np.pi / 2]]))


def test_rmsd_and_least_rmsd_kernels():
    reference = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        dtype=np.float64,
    )
    shifted = reference + np.array([1.0, 2.0, 3.0], dtype=np.float64)

    assert np.isclose(get_rmsd_single_structure(reference, reference), 0.0)
    assert np.isclose(get_least_rmsd_single_structure(reference, shifted), 0.0)

    batch_reference = reference[np.newaxis, :, :]
    batch_shifted = shifted[np.newaxis, :, :]
    np.testing.assert_allclose(get_rmsd(batch_reference, batch_reference), np.array([0.0]))
    np.testing.assert_allclose(get_rmsd_with_single_reference_structure(batch_shifted, reference), np.array([np.sqrt(14.0)]))
    np.testing.assert_allclose(get_least_rmsd(batch_shifted, batch_reference), np.array([0.0]))
    np.testing.assert_allclose(get_least_rmsd_with_single_reference_structure(batch_shifted, reference), np.array([0.0]))


def test_component_index_kernel_handles_disconnected_and_empty_cases():
    bonded = np.array([[0, 1], [1, 2], [4, 5]], dtype=np.int64)
    out = get_component_index_from_bonded_atom_pairs(bonded, 6)
    np.testing.assert_array_equal(out, np.array([0, 0, 0, 1, 2, 2], dtype=np.int64))

    empty = get_component_index_from_bonded_atom_pairs(np.empty((0, 2), dtype=np.int64), 0)
    assert empty.shape == (0,)
