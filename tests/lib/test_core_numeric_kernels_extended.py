import numpy as np

from molsysmt.lib.pbc.get_box_from_lengths_and_angles import (
    get_box_from_lengths_and_angles,
    get_box_from_lengths_and_angles_single_structure,
)
from molsysmt.lib.pbc.get_lengths_and_angles_from_box import (
    get_lengths_and_angles_from_box,
    get_lengths_and_angles_from_box_single_structure,
)
from molsysmt.lib.pbc.wrap_to_mic import wrap_to_mic, wrap_to_mic_vector_single_structure
from molsysmt.lib.pbc.wrap_to_pbc import (
    wrap_to_pbc,
    wrap_to_pbc_center,
    wrap_to_pbc_vector_single_structure,
    wrap_to_pbc_center_vector_single_structure,
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
from molsysmt.lib.structure.get_angles import get_angles, get_angles_single_structure
from molsysmt.lib.structure.get_dihedral_angles import (
    get_dihedral_angles,
    get_dihedral_angles_single_structure,
)
from molsysmt.lib.structure.get_rmsd import (
    get_rmsd,
    get_rmsd_single_structure,
    get_rmsd_with_single_reference_structure,
)
from molsysmt.lib.structure.get_least_rmsd import (
    get_least_rmsd,
    get_least_rmsd_single_structure,
    get_least_rmsd_with_single_reference_structure,
)
from molsysmt.lib.topology.get_component_index_from_bonded_atom_pairs import (
    get_component_index_from_bonded_atom_pairs,
)


def test_box_roundtrip_single_and_multiple_structures():
    lengths = np.array([2.0, 3.0, 4.0], dtype=np.float64)
    angles = np.array([np.pi / 2, np.pi / 2, np.pi / 2], dtype=np.float64)
    box = get_box_from_lengths_and_angles_single_structure(lengths, angles)
    recovered_lengths, recovered_angles = get_lengths_and_angles_from_box_single_structure(box)
    assert np.allclose(recovered_lengths, lengths)
    assert np.allclose(recovered_angles, angles)

    lengths_many = np.array([[2.0, 3.0, 4.0], [5.0, 6.0, 7.0]], dtype=np.float64)
    angles_many = np.array(
        [[np.pi / 2, np.pi / 2, np.pi / 2], [np.pi / 2, np.pi / 2, 2.0 * np.pi / 3]],
        dtype=np.float64,
    )
    boxes = get_box_from_lengths_and_angles(lengths_many, angles_many)
    out_lengths, out_angles = get_lengths_and_angles_from_box(boxes)
    assert np.allclose(out_lengths, lengths_many)
    assert np.allclose(out_angles, angles_many)


def test_wrap_kernels_cover_single_vector_and_batched_coordinates():
    orth_box = np.diag(np.array([2.0, 2.0, 2.0], dtype=np.float64))
    vector = np.array([2.7, -0.2, 1.1], dtype=np.float64)

    wrapped_mic = wrap_to_mic_vector_single_structure(vector, orth_box, None, None)
    assert np.all(np.abs(wrapped_mic) <= 1.0 + 1e-12)

    wrapped_pbc = wrap_to_pbc_vector_single_structure(vector, orth_box, None, None)
    assert np.all((wrapped_pbc >= -1e-12) & (wrapped_pbc < 2.0 + 1e-12))

    wrapped_pbc_center = wrap_to_pbc_center_vector_single_structure(vector, orth_box, None, None)
    assert np.all(np.abs(wrapped_pbc_center) <= 1.0 + 1e-12)

    triclinic_box = get_box_from_lengths_and_angles_single_structure(
        np.array([2.0, 3.0, 4.0], dtype=np.float64),
        np.array([np.pi / 2, np.pi / 2, 2.0 * np.pi / 3], dtype=np.float64),
    )
    triclinic_vector = np.array([3.1, 2.4, 4.7], dtype=np.float64)
    _ = wrap_to_mic_vector_single_structure(triclinic_vector, triclinic_box, None, None)
    _ = wrap_to_pbc_vector_single_structure(triclinic_vector, triclinic_box, None, None)
    _ = wrap_to_pbc_center_vector_single_structure(triclinic_vector, triclinic_box, None, None)

    coordinates = np.array([[[2.7, -0.2, 1.1], [4.1, 4.2, -0.1]]], dtype=np.float64)
    box = np.array([orth_box], dtype=np.float64)
    wrap_to_mic(coordinates, box, np.zeros(3, dtype=np.float64))
    assert np.all(np.abs(coordinates) <= 1.0 + 1e-12)

    coordinates = np.array([[[2.7, -0.2, 1.1], [4.1, 4.2, -0.1]]], dtype=np.float64)
    wrap_to_pbc(coordinates, box, np.zeros(3, dtype=np.float64))
    assert np.all((coordinates >= -1e-12) & (coordinates < 2.0 + 1e-12))

    coordinates = np.array([[[2.7, -0.2, 1.1], [4.1, 4.2, -0.1]]], dtype=np.float64)
    wrap_to_pbc_center(coordinates, box, np.zeros(3, dtype=np.float64))
    assert np.all(np.abs(coordinates) <= 1.0 + 1e-12)


def test_distance_kernels_cover_all_entry_points():
    p1 = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    p2 = np.array([1.0, 0.0, 0.0], dtype=np.float64)
    assert np.isclose(get_distance_two_points_single_structure(p1, p2), 1.0)

    coords_a_single = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], dtype=np.float64)
    coords_b_single = np.array([[0.0, 1.0, 0.0], [1.0, 1.0, 0.0]], dtype=np.float64)

    distances_single_system = get_distances_single_system_single_structure(coords_a_single)
    assert distances_single_system.shape == (2, 2)
    assert np.isclose(distances_single_system[0, 1], 1.0)

    distances_single_structure = get_distances_single_structure(coords_a_single, coords_b_single)
    assert distances_single_structure.shape == (2, 2)

    pairwise_single = get_distances_pairs_single_structure(coords_a_single, coords_b_single)
    assert pairwise_single.shape == (2,)
    assert np.allclose(pairwise_single, [1.0, 1.0])

    coords_a = np.array([coords_a_single, coords_a_single + 1.0], dtype=np.float64)
    coords_b = np.array([coords_b_single, coords_b_single + 1.0], dtype=np.float64)

    distances_many = get_distances(coords_a, coords_b)
    assert distances_many.shape == (2, 2, 2)

    distances_single_system_many = get_distances_single_system(coords_a)
    assert distances_single_system_many.shape == (2, 2, 2)

    pairwise_many = get_distances_pairs(coords_a, coords_b)
    assert pairwise_many.shape == (2, 2)
    assert np.allclose(pairwise_many, 1.0)


def test_angle_and_dihedral_kernels_cover_single_and_multiple_structures():
    coords_single = np.array(
        [[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 1.0]],
        dtype=np.float64,
    )
    triplets = np.array([[0, 1, 2]], dtype=np.int64)
    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)

    angle_single = get_angles_single_structure(coords_single, triplets)
    assert angle_single.shape == (1,)
    assert np.isclose(angle_single[0], np.pi / 2)

    dihedral_single = get_dihedral_angles_single_structure(coords_single, quartets)
    assert dihedral_single.shape == (1,)
    assert np.isclose(abs(dihedral_single[0]), np.pi / 2)

    coords_many = np.array([coords_single, coords_single + 1.0], dtype=np.float64)
    angle_many = get_angles(coords_many, triplets)
    dihedral_many = get_dihedral_angles(coords_many, quartets)
    assert angle_many.shape == (2, 1)
    assert dihedral_many.shape == (2, 1)


def test_rmsd_kernels_cover_single_and_multiple_reference_paths():
    ref_single = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], dtype=np.float64)
    coords_single = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 0.0]], dtype=np.float64)
    expected = np.sqrt(0.5)

    assert np.isclose(get_rmsd_single_structure(coords_single, ref_single), expected)
    assert np.isclose(get_least_rmsd_single_structure(coords_single, coords_single), 0.0)

    coords_many = np.array([coords_single, ref_single], dtype=np.float64)
    refs_many = np.array([ref_single, ref_single], dtype=np.float64)

    rmsd_many = get_rmsd(coords_many, refs_many)
    assert rmsd_many.shape == (2,)
    assert np.isclose(rmsd_many[0], expected)
    assert np.isclose(rmsd_many[1], 0.0)

    rmsd_single_ref = get_rmsd_with_single_reference_structure(coords_many, ref_single)
    assert rmsd_single_ref.shape == (2,)

    least_many = get_least_rmsd(coords_many, refs_many)
    least_single_ref = get_least_rmsd_with_single_reference_structure(coords_many, ref_single)
    assert least_many.shape == (2,)
    assert least_single_ref.shape == (2,)
    assert np.isclose(least_many[1], 0.0)
    assert np.isclose(least_single_ref[1], 0.0)


def test_component_index_kernel_handles_bonds_and_isolated_atoms():
    bonded_atom_pairs = np.array([[0, 1], [1, 2], [4, 5]], dtype=np.int64)
    component_index = get_component_index_from_bonded_atom_pairs(bonded_atom_pairs, 7)
    assert component_index.tolist() == [0, 0, 0, 1, 2, 2, 3]

    empty = get_component_index_from_bonded_atom_pairs(np.empty((0, 2), dtype=np.int64), 3)
    assert empty.tolist() == [0, 1, 2]
