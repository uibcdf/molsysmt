import numpy as np

from molsysmt.lib.structure.get_principal_geometric_axes import get_principal_geometric_axes_single_structure, get_principal_geometric_axes
from molsysmt.lib.structure.get_principal_inertia_axes import get_principal_inertia_axes_single_structure, get_principal_inertia_axes
from molsysmt.lib.structure.principal_component_analysis import principal_component_analysis


def test_axes_and_pca_with_weight_variants():
    coords = np.array([[0.,0.,0.],[1.,0.,0.],[0.,2.,0.],[0.,0.,3.]], dtype=np.float64)
    batch = np.stack([coords, coords + 0.2, coords + np.array([0.1, -0.1, 0.05])])
    weights = np.array([1., 2., 3., 4.], dtype=np.float64)

    evals_g, evecs_g = get_principal_geometric_axes_single_structure(coords, weights)
    assert evals_g.shape == (3,)
    assert evecs_g.shape == (3,3)
    assert np.allclose(evecs_g.T @ evecs_g, np.eye(3), atol=1e-6)

    evals_g_b, evecs_g_b = get_principal_geometric_axes(batch, weights)
    assert evals_g_b.shape == (3,3)
    assert evecs_g_b.shape == (3,3,3)

    evals_i, evecs_i = get_principal_inertia_axes_single_structure(coords, weights)
    assert evals_i.shape == (3,)
    assert evecs_i.shape == (3,3)

    evals_i_b, evecs_i_b = get_principal_inertia_axes(batch, weights)
    assert evals_i_b.shape == (3,3)
    assert evecs_i_b.shape == (3,3,3)

    pca_vals, pca_vecs = principal_component_analysis(batch, weights)
    assert pca_vals.ndim == 1
    assert pca_vecs.shape[0] == pca_vals.shape[0]
