import numpy as np

from molsysmt.lib.structure.get_dihedral_angles import (
    get_dihedral_angles,
    get_dihedral_angles_single_structure,
)
from molsysmt.lib.structure.get_mic_dihedral_angles import get_mic_dihedral_angles
from molsysmt.lib.structure.set_dihedral_angles import (
    set_dihedral_angles,
    set_dihedral_angles_single_structure,
)
from molsysmt.lib.structure.set_mic_dihedral_angles import set_mic_dihedral_angles
from molsysmt.lib.structure.shift_dihedral_angles import (
    shift_dihedral_angles,
    shift_dihedral_angles_single_structure,
)
from molsysmt.lib.structure.principal_component_analysis import principal_component_analysis
from molsysmt.lib.structure.get_principal_geometric_axes import (
    get_principal_geometric_axes,
    get_principal_geometric_axes_single_structure,
)
from molsysmt.lib.structure.get_principal_inertia_axes import (
    get_principal_inertia_axes,
    get_principal_inertia_axes_single_structure,
)


def _reference_coordinates():
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0],
        ],
        dtype=np.float64,
    )


def test_set_and_shift_dihedral_kernels_match_expected_angles():
    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    blocks = np.array([[False, False, False, True]], dtype=np.bool_)
    coordinates = _reference_coordinates()

    target_angle = np.array([np.pi / 2], dtype=np.float64)
    set_single = coordinates.copy()
    set_dihedral_angles_single_structure(set_single, target_angle, quartets, blocks)
    np.testing.assert_allclose(
        get_dihedral_angles_single_structure(set_single, quartets),
        target_angle,
        atol=1e-12,
    )

    batched = coordinates[np.newaxis, :, :].copy()
    set_dihedral_angles(batched, target_angle[np.newaxis, :], quartets, blocks)
    np.testing.assert_allclose(
        get_dihedral_angles_single_structure(batched[0], quartets),
        target_angle,
        atol=1e-12,
    )

    shift_single = coordinates.copy()
    shift_dihedral_angles_single_structure(
        shift_single,
        np.array([np.pi], dtype=np.float64),
        quartets,
        blocks,
    )
    np.testing.assert_allclose(
        get_dihedral_angles_single_structure(shift_single, quartets),
        np.array([np.pi / 2], dtype=np.float64),
        atol=1e-12,
    )

    shifted_batch = coordinates[np.newaxis, :, :].copy()
    shift_dihedral_angles(
        shifted_batch,
        np.array([[np.pi]], dtype=np.float64),
        quartets,
        blocks,
        np.array([0], dtype=np.int64),
    )
    np.testing.assert_allclose(
        get_dihedral_angles_single_structure(shifted_batch[0], quartets),
        np.array([np.pi / 2], dtype=np.float64),
        atol=1e-12,
    )


def test_set_dihedral_angles_broadcasts_one_target_row_on_both_paths():
    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    blocks = np.array([[False, False, False, True]], dtype=np.bool_)
    coordinates = np.repeat(_reference_coordinates()[np.newaxis, :, :], 3, axis=0)
    boxes = np.repeat((10.0 * np.eye(3))[np.newaxis, :, :], 3, axis=0)
    target = np.array([[np.pi / 3]], dtype=np.float64)
    expected = np.repeat(target, 3, axis=0)

    vacuum_coordinates = coordinates.copy()
    set_dihedral_angles(vacuum_coordinates, target, quartets, blocks)
    np.testing.assert_allclose(
        get_dihedral_angles(vacuum_coordinates, quartets),
        expected,
        atol=1e-12,
    )

    periodic_coordinates = coordinates.copy()
    set_mic_dihedral_angles(periodic_coordinates, boxes, target, quartets, blocks)
    np.testing.assert_allclose(
        get_mic_dihedral_angles(periodic_coordinates, boxes, quartets),
        expected,
        atol=1e-12,
    )


def test_principal_component_analysis_returns_sorted_eigendecomposition_shapes():
    coordinates = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]],
        ],
        dtype=np.float64,
    )
    weights = np.ones(2, dtype=np.float64)

    eigenvalues, eigenvectors = principal_component_analysis(coordinates, weights)

    assert eigenvalues.shape == (6,)
    assert eigenvectors.shape == (6, 6)
    assert np.all(np.diff(eigenvalues) >= -1e-12)
    np.testing.assert_allclose(eigenvectors @ eigenvectors.T, np.eye(6), atol=1e-10)


def test_principal_axes_kernels_return_orthonormal_axes_for_single_and_batch_paths():
    coordinates = np.array(
        [
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 2.0, 0.0],
            [0.0, -2.0, 0.0],
        ],
        dtype=np.float64,
    )
    weights = np.array([1.0, 1.0, 2.0, 2.0], dtype=np.float64)

    geo_values, geo_vectors = get_principal_geometric_axes_single_structure(coordinates, weights)
    inertia_values, inertia_vectors = get_principal_inertia_axes_single_structure(coordinates, weights)

    assert geo_values.shape == (3,)
    assert inertia_values.shape == (3,)
    np.testing.assert_allclose(geo_vectors.T @ geo_vectors, np.eye(3), atol=1e-10)
    np.testing.assert_allclose(inertia_vectors @ inertia_vectors.T, np.eye(3), atol=1e-10)

    batch = np.stack([coordinates, coordinates * 1.5], axis=0)
    geo_values_batch, geo_vectors_batch = get_principal_geometric_axes(batch, weights)
    inertia_values_batch, inertia_vectors_batch = get_principal_inertia_axes(batch, weights)

    assert geo_values_batch.shape == (2, 3)
    assert geo_vectors_batch.shape == (2, 3, 3)
    assert inertia_values_batch.shape == (2, 3)
    assert inertia_vectors_batch.shape == (2, 3, 3)
    np.testing.assert_allclose(geo_vectors_batch[0].T @ geo_vectors_batch[0], np.eye(3), atol=1e-10)
    np.testing.assert_allclose(inertia_vectors_batch[0] @ inertia_vectors_batch[0].T, np.eye(3), atol=1e-10)
