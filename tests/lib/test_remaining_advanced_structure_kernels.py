import math
import numpy as np

from molsysmt.lib.structure.get_least_rmsd_rotation_and_translation import (
    get_least_rmsd_rotation_and_translation_single_structure,
    get_least_rmsd_rotation_and_translation,
    get_least_rmsd_rotation_and_translation_with_single_reference_structure,
)
from molsysmt.lib.structure.get_mic_distances import (
    get_mic_distance_two_points_single_structure,
    get_mic_distances_single_system,
    get_mic_distances,
    get_mic_distances_pairs,
    get_mic_distances_single_system_single_structure,
    get_mic_distances_single_structure,
    get_mic_distances_pairs_single_structure,
)
from molsysmt.lib.structure.get_mic_angles import (
    get_mic_angles_single_structure,
    get_mic_angles,
)
from molsysmt.lib.structure.get_mic_dihedral_angles import (
    get_mic_dihedral_angles_single_structure,
    get_mic_dihedral_angles,
)
from molsysmt.lib.structure.get_principal_geometric_axes import (
    get_principal_geometric_axes_single_structure,
    get_principal_geometric_axes,
)
from molsysmt.lib.structure.get_principal_inertia_axes import (
    get_principal_inertia_axes_single_structure,
    get_principal_inertia_axes,
)
from molsysmt.lib.structure.principal_component_analysis import principal_component_analysis
from molsysmt.lib.structure.set_mic_dihedral_angles import (
    set_mic_dihedral_angles_single_structure,
    set_mic_dihedral_angles,
)
from molsysmt.lib.structure.shift_mic_dihedral_angles import (
    shift_mic_dihedral_angles_single_structure,
    shift_mic_dihedral_angles,
)


def _orthogonal_box():
    return np.diag([3.0, 3.0, 3.0]).astype(np.float64)


def _base_coords():
    return np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0]],
        dtype=np.float64,
    )


def test_rotation_translation_and_axes_kernels():
    ref = _base_coords()
    moved = ref + np.array([2.0, -1.0, 0.5], dtype=np.float64)

    center_rotation, rotation, translation = get_least_rmsd_rotation_and_translation_single_structure(moved, ref)
    assert center_rotation.shape == (3,)
    assert rotation.shape == (3, 3)
    assert translation.shape == (3,)
    assert np.allclose(rotation @ rotation.T, np.eye(3), atol=1e-6)

    batch_moved = np.stack([moved, ref])
    batch_ref = np.stack([ref, ref])
    c_batch, r_batch, t_batch = get_least_rmsd_rotation_and_translation(batch_moved, batch_ref)
    assert c_batch.shape == (2, 1, 3)
    assert r_batch.shape == (2, 1, 3, 3)
    assert t_batch.shape == (2, 1, 3)

    c_single_ref, r_single_ref, t_single_ref = get_least_rmsd_rotation_and_translation_with_single_reference_structure(batch_moved, ref)
    assert c_single_ref.shape == (2, 1, 3)
    assert r_single_ref.shape == (2, 1, 3, 3)
    assert t_single_ref.shape == (2, 1, 3)

    weights = np.array([1.0, 1.0, 2.0, 2.0], dtype=np.float64)
    evals_g, evecs_g = get_principal_geometric_axes_single_structure(ref, weights)
    assert evals_g.shape == (3,)
    assert evecs_g.shape == (3, 3)
    assert np.allclose(evecs_g.T @ evecs_g, np.eye(3), atol=1e-6)

    evals_g_b, evecs_g_b = get_principal_geometric_axes(np.stack([ref, moved]), weights)
    assert evals_g_b.shape == (2, 3)
    assert evecs_g_b.shape == (2, 3, 3)

    evals_i, evecs_i = get_principal_inertia_axes_single_structure(ref, weights)
    assert evals_i.shape == (3,)
    assert evecs_i.shape == (3, 3)
    assert np.allclose(evecs_i @ evecs_i.T, np.eye(3), atol=1e-6)

    evals_i_b, evecs_i_b = get_principal_inertia_axes(np.stack([ref, moved]), weights)
    assert evals_i_b.shape == (2, 3)
    assert evecs_i_b.shape == (2, 3, 3)

    pca_evals, pca_evecs = principal_component_analysis(np.stack([ref, moved, ref + 0.1]), weights)
    assert pca_evals.ndim == 1
    assert pca_evecs.shape[0] == pca_evals.shape[0]


def test_mic_distance_angle_dihedral_and_mutation_kernels():
    box = _orthogonal_box()
    coords = _base_coords()
    batch_coords = np.stack([coords, coords + 0.2])
    batch_box = np.stack([box, box])

    d = get_mic_distance_two_points_single_structure(np.array([0.0, 0.0, 0.0]), np.array([2.8, 0.0, 0.0]), box, None, None)
    assert math.isclose(d, 0.2, rel_tol=1e-6)

    d_single_system_single = get_mic_distances_single_system_single_structure(coords[:3], box)
    assert d_single_system_single.shape == (3, 3)

    d_single_system = get_mic_distances_single_system(batch_coords[:, :3, :], batch_box)
    assert d_single_system.shape == (2, 3, 3)

    d_cross_single = get_mic_distances_single_structure(coords[:2], coords[2:], box)
    assert d_cross_single.shape == (2, 2)

    d_cross = get_mic_distances(batch_coords[:, :2, :], batch_coords[:, 2:, :], batch_box)
    assert d_cross.shape == (2, 2, 2)

    d_pairs_single = get_mic_distances_pairs_single_structure(coords[:2], coords[2:], box)
    assert d_pairs_single.shape == (2,)

    d_pairs = get_mic_distances_pairs(batch_coords[:, :2, :], batch_coords[:, 2:, :], batch_box)
    assert d_pairs.shape == (2, 2)

    triplets = np.array([[0, 1, 2]], dtype=np.int64)
    ang_single = get_mic_angles_single_structure(coords, box, triplets)
    assert np.allclose(ang_single, np.array([math.pi / 2]))
    ang_batch = get_mic_angles(batch_coords, batch_box, triplets)
    assert ang_batch.shape == (2, 1)

    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    dih_single = get_mic_dihedral_angles_single_structure(coords, box, quartets)
    assert np.allclose(dih_single, np.array([math.pi / 2]))
    dih_batch = get_mic_dihedral_angles(batch_coords, batch_box, quartets)
    assert dih_batch.shape == (2, 1)

    blocks = np.array([[False, False, False, True]], dtype=np.bool_)

    coords_set = coords.copy()
    set_mic_dihedral_angles_single_structure(coords_set, box, np.array([0.0], dtype=np.float64), quartets, blocks)
    assert not np.allclose(coords_set[3], coords[3])

    coords_set_batch = np.stack([coords.copy(), coords.copy()])
    set_mic_dihedral_angles(coords_set_batch, batch_box, np.array([[0.0], [0.0]], dtype=np.float64), quartets, blocks)
    assert coords_set_batch.shape == (2, 4, 3)

    coords_shift = coords.copy()
    shift_mic_dihedral_angles_single_structure(coords_shift, box, np.array([0.1], dtype=np.float64), quartets, blocks)
    assert not np.allclose(coords_shift[3], coords[3])

    coords_shift_batch = np.stack([coords.copy(), coords.copy()])
    shift_mic_dihedral_angles(
        coords_shift_batch,
        batch_box,
        np.array([[0.1], [0.1]], dtype=np.float64),
        quartets,
        blocks,
        np.array([0, 1], dtype=np.int64),
    )
    assert coords_shift_batch.shape == (2, 4, 3)
