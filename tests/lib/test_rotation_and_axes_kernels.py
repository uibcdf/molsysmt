import numpy as np

from molsysmt.lib.structure.get_least_rmsd_rotation_and_translation import (
    get_least_rmsd_rotation_and_translation,
    get_least_rmsd_rotation_and_translation_single_structure,
    get_least_rmsd_rotation_and_translation_with_single_reference_structure,
)
from molsysmt.lib.structure.get_principal_geometric_axes import (
    get_principal_geometric_axes,
    get_principal_geometric_axes_single_structure,
)
from molsysmt.lib.structure.get_principal_inertia_axes import (
    get_principal_inertia_axes,
    get_principal_inertia_axes_single_structure,
)
from molsysmt.lib.structure.principal_component_analysis import principal_component_analysis


def test_least_rmsd_rotation_and_translation_helpers_cover_all_entry_points():
    reference = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        dtype=np.float64,
    )
    shifted = reference + np.array([2.0, -1.0, 0.5], dtype=np.float64)

    center_rotation, rotation, translation = get_least_rmsd_rotation_and_translation_single_structure(
        shifted, reference
    )
    np.testing.assert_allclose(center_rotation, np.array([2.3333333333333335, -0.6666666666666666, 0.5]), atol=1e-12)
    np.testing.assert_allclose(rotation @ rotation.T, np.eye(3), atol=1e-10)
    np.testing.assert_allclose(translation, np.array([-2.0, 1.0, -0.5]), atol=1e-12)

    batch_shifted = np.stack([shifted, shifted + 1.0], axis=0)
    batch_reference = np.stack([reference, reference + 1.0], axis=0)
    center_rotation_batch, rotation_batch, translation_batch = get_least_rmsd_rotation_and_translation(
        batch_shifted, batch_reference
    )
    assert center_rotation_batch.shape == (2, 1, 3)
    assert rotation_batch.shape == (2, 1, 3, 3)
    assert translation_batch.shape == (2, 1, 3)

    center_rotation_single_ref, rotation_single_ref, translation_single_ref = (
        get_least_rmsd_rotation_and_translation_with_single_reference_structure(batch_shifted, reference)
    )
    assert center_rotation_single_ref.shape == (2, 1, 3)
    assert rotation_single_ref.shape == (2, 1, 3, 3)
    assert translation_single_ref.shape == (2, 1, 3)


def test_principal_axes_and_pca_helpers_cover_single_and_batch_paths():
    coordinates = np.array(
        [[1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, -2.0, 0.0]],
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

    pca_coordinates = np.array(
        [
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]],
        ],
        dtype=np.float64,
    )
    eigenvalues, eigenvectors = principal_component_analysis(pca_coordinates, np.ones(2, dtype=np.float64))
    assert eigenvalues.shape == (6,)
    assert eigenvectors.shape == (6, 6)
    assert np.all(np.diff(eigenvalues) >= -1e-12)
