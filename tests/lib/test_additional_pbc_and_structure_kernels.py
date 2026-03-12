import math
import numpy as np

from molsysmt.lib.pbc.box_is_orthogonal import (
    box_is_orthogonal_single_structure,
    box_is_orthogonal,
)
from molsysmt.lib.pbc.get_box_from_lengths_and_angles import (
    get_box_from_lengths_and_angles_single_structure,
    get_box_from_lengths_and_angles,
)
from molsysmt.lib.pbc.get_lengths_and_angles_from_box import (
    get_lengths_and_angles_from_box_single_structure,
    get_lengths_and_angles_from_box,
)
from molsysmt.lib.pbc.wrap_to_mic import wrap_to_mic_vector_single_structure, wrap_to_mic
from molsysmt.lib.pbc.wrap_to_pbc import (
    wrap_to_pbc_vector_single_structure,
    wrap_to_pbc_center_vector_single_structure,
    wrap_to_pbc,
    wrap_to_pbc_center,
)
from molsysmt.lib.structure.get_distances import (
    get_distance_two_points_single_structure,
    get_distances_single_system,
    get_distances,
    get_distances_pairs,
    get_distances_single_system_single_structure,
    get_distances_single_structure,
    get_distances_pairs_single_structure,
)
from molsysmt.lib.structure.get_angles import get_angles_single_structure, get_angles
from molsysmt.lib.structure.get_dihedral_angles import (
    get_dihedral_angles_single_structure,
    get_dihedral_angles,
)
from molsysmt.lib.structure.get_center import (
    get_center_single_structure,
    get_center,
    get_center_groups_of_atoms_single_structure,
    get_center_groups_of_atoms,
)
from molsysmt.lib.structure.flip import flip_single_structure, flip
from molsysmt.lib.structure.get_rmsd import (
    get_rmsd_single_structure,
    get_rmsd,
    get_rmsd_with_single_reference_structure,
)
from molsysmt.lib.structure.get_least_rmsd import (
    get_least_rmsd_single_structure,
    get_least_rmsd,
    get_least_rmsd_with_single_reference_structure,
)
from molsysmt.lib.structure.set_dihedral_angles import (
    set_dihedral_angles_single_structure,
    set_dihedral_angles,
)
from molsysmt.lib.structure.shift_dihedral_angles import (
    shift_dihedral_angles_single_structure,
    shift_dihedral_angles,
)


def test_box_and_wrap_kernels():
    ortho_box = np.diag([2.0, 3.0, 4.0]).astype(np.float64)
    triclinic_lengths = np.array([2.0, 3.0, 4.0], dtype=np.float64)
    triclinic_angles = np.array([1.3, 1.4, 1.2], dtype=np.float64)
    triclinic_box = get_box_from_lengths_and_angles_single_structure(triclinic_lengths, triclinic_angles)

    assert box_is_orthogonal_single_structure(ortho_box)
    assert not box_is_orthogonal_single_structure(triclinic_box)
    flags = box_is_orthogonal(np.stack([ortho_box, triclinic_box]))
    assert flags.tolist() == [True, False]

    batch_boxes = get_box_from_lengths_and_angles(
        np.stack([triclinic_lengths, triclinic_lengths]),
        np.stack([triclinic_angles, triclinic_angles]),
    )
    assert batch_boxes.shape == (2, 3, 3)

    lengths_back, angles_back = get_lengths_and_angles_from_box_single_structure(triclinic_box)
    assert np.allclose(lengths_back, triclinic_lengths)
    assert np.allclose(angles_back, triclinic_angles)
    lengths_batch, angles_batch = get_lengths_and_angles_from_box(np.stack([triclinic_box, triclinic_box]))
    assert np.allclose(lengths_batch[0], triclinic_lengths)
    assert np.allclose(angles_batch[1], triclinic_angles)

    vector = np.array([2.6, -1.6, 4.4], dtype=np.float64)
    mic_vec = wrap_to_mic_vector_single_structure(vector, ortho_box, None, None)
    assert np.allclose(mic_vec, np.array([0.6, 1.4, 0.4]))
    pbc_vec = wrap_to_pbc_vector_single_structure(vector, ortho_box, None, None)
    assert np.allclose(pbc_vec, np.array([0.6, 1.4, 0.4]))
    centered = wrap_to_pbc_center_vector_single_structure(vector, ortho_box, None, None)
    assert np.allclose(centered, np.array([0.6, 1.4, 0.4]))

    coordinates = np.array([[[2.6, -1.6, 4.4], [0.2, 0.2, 0.2]]], dtype=np.float64)
    wrap_to_mic(coordinates, np.array([ortho_box]), np.zeros(3, dtype=np.float64))
    assert np.allclose(coordinates[0, 0], np.array([0.6, 1.4, 0.4]))

    coordinates = np.array([[[2.6, -1.6, 4.4], [0.2, 0.2, 0.2]]], dtype=np.float64)
    wrap_to_pbc(coordinates, np.array([ortho_box]), np.zeros(3, dtype=np.float64))
    assert np.allclose(coordinates[0, 0], np.array([0.6, 1.4, 0.4]))

    coordinates = np.array([[[1.6, 2.1, 2.6], [0.2, 0.2, 0.2]]], dtype=np.float64)
    wrap_to_pbc_center(coordinates, np.array([ortho_box]), np.array([1.0, 1.5, 2.0], dtype=np.float64))
    assert np.all(coordinates[0, 0] <= np.array([2.0, 3.0, 4.0]))


def test_distance_angle_dihedral_center_and_flip_kernels():
    coords_single = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0]],
        dtype=np.float64,
    )
    coords = np.array([coords_single, coords_single + 1.0], dtype=np.float64)

    assert math.isclose(get_distance_two_points_single_structure(coords_single[0], coords_single[1]), 1.0)
    dmat_single = get_distances_single_system_single_structure(coords_single[:3])
    assert dmat_single.shape == (3, 3)
    assert np.allclose(dmat_single, dmat_single.T)

    dmat = get_distances_single_system(coords[:, :3, :])
    assert dmat.shape == (2, 3, 3)

    cross = get_distances(coords[:, :2, :], coords[:, 2:, :])
    assert cross.shape == (2, 2, 2)

    pairs = get_distances_pairs(coords[:, :2, :], coords[:, 2:, :])
    assert pairs.shape == (2, 2)

    cross_single = get_distances_single_structure(coords_single[:2], coords_single[2:])
    assert cross_single.shape == (2, 2)

    pairs_single = get_distances_pairs_single_structure(coords_single[:2], coords_single[2:])
    assert pairs_single.shape == (2,)

    triplets = np.array([[0, 1, 2]], dtype=np.int64)
    angles_single = get_angles_single_structure(coords_single, triplets)
    assert np.allclose(angles_single, np.array([math.pi / 2]))
    angles_batch = get_angles(coords, triplets)
    assert angles_batch.shape == (2, 1)

    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    dihed_single = get_dihedral_angles_single_structure(coords_single, quartets)
    assert np.allclose(dihed_single, np.array([math.pi / 2]))
    dihed_batch = get_dihedral_angles(coords, quartets)
    assert dihed_batch.shape == (2, 1)

    weights = np.array([1.0, 1.0, 2.0, 2.0], dtype=np.float64)
    center_single = get_center_single_structure(coords_single, weights)
    assert center_single.shape == (3,)
    center_batch = get_center(coords, weights)
    assert center_batch.shape == (2, 1, 3)

    atoms_per_group = np.array([2, 2], dtype=np.int64)
    center_groups_single = get_center_groups_of_atoms_single_structure(coords_single, atoms_per_group, weights)
    assert center_groups_single.shape == (2, 3)
    center_groups = get_center_groups_of_atoms(coords, atoms_per_group, weights)
    assert center_groups.shape == (2, 2, 3)

    flipped_single = flip_single_structure(coords_single, np.array([1.0, 0.0, 0.0]), np.zeros(3))
    assert np.allclose(flipped_single[:, 0], -coords_single[:, 0])
    flipped = flip(coords, np.array([0.0, 1.0, 0.0]), np.zeros(3))
    assert np.allclose(flipped[:, :, 1], -coords[:, :, 1])


def test_rmsd_and_dihedral_mutation_kernels():
    ref_single = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0]],
        dtype=np.float64,
    )
    moved_single = ref_single.copy()
    moved_single[3] = np.array([2.0, 1.0, 1.0], dtype=np.float64)

    ref = np.array([ref_single, ref_single], dtype=np.float64)
    moved = np.array([moved_single, ref_single], dtype=np.float64)

    rmsd_single = get_rmsd_single_structure(moved_single, ref_single)
    assert rmsd_single > 0.0
    rmsd_batch = get_rmsd(moved, ref)
    assert rmsd_batch.shape == (2,)
    rmsd_single_ref = get_rmsd_with_single_reference_structure(moved, ref_single)
    assert rmsd_single_ref.shape == (2,)

    least_single = get_least_rmsd_single_structure(ref_single, ref_single)
    assert math.isclose(least_single, 0.0, abs_tol=1e-12)
    least_batch = get_least_rmsd(ref, ref)
    assert np.allclose(least_batch, np.zeros(2))
    least_single_ref = get_least_rmsd_with_single_reference_structure(ref, ref_single)
    assert np.allclose(least_single_ref, np.zeros(2))

    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    blocks = np.array([[False, False, False, True]], dtype=np.bool_)

    coords_for_set = np.array(ref_single.copy(), dtype=np.float64)
    set_dihedral_angles_single_structure(coords_for_set, np.array([0.0], dtype=np.float64), quartets, blocks)
    assert not np.allclose(coords_for_set[3], ref_single[3])

    coords_for_set_batch = np.array([ref_single.copy(), ref_single.copy()], dtype=np.float64)
    set_dihedral_angles(coords_for_set_batch, np.array([[0.0], [0.0]], dtype=np.float64), quartets, blocks)
    assert coords_for_set_batch.shape == (2, 4, 3)

    coords_for_shift = np.array(ref_single.copy(), dtype=np.float64)
    shift_dihedral_angles_single_structure(coords_for_shift, np.array([0.1], dtype=np.float64), quartets, blocks)
    assert not np.allclose(coords_for_shift[3], ref_single[3])

    coords_for_shift_batch = np.array([ref_single.copy(), ref_single.copy()], dtype=np.float64)
    shift_dihedral_angles(
        coords_for_shift_batch,
        np.array([[0.1], [0.1]], dtype=np.float64),
        quartets,
        blocks,
        np.array([0, 1], dtype=np.int64),
    )
    assert coords_for_shift_batch.shape == (2, 4, 3)
