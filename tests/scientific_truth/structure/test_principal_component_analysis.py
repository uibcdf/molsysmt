"""Analytic scientific truth tests for the current PCA numerical core."""

import itertools

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def test_pca_matches_closed_form_diagonal_covariance(float64_kernel_atol):
    """Recover exact eigenvalues and axes from independent sign combinations."""

    coordinates = np.array(
        [
            [[sign_x, 2.0 * sign_y, 3.0 * sign_z]]
            for sign_x, sign_y, sign_z in itertools.product((-1.0, 1.0), repeat=3)
        ],
        dtype=np.float64,
    )
    system = Structures(coordinates=coordinates * msm.pyunitwizard.unit("nm"))

    eigenvectors, eigenvalues = msm.structure.principal_component_analysis(
        system, selection="all", use_gpu=False
    )

    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(eigenvalues, to_unit="nm**2"),
        np.array([9.0, 4.0, 1.0]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        np.abs(eigenvectors),
        np.eye(3)[::-1],
        rtol=0.0,
        atol=float64_kernel_atol,
    )
