"""Analytic scientific truth tests for rigid structural alignment."""

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def test_least_rmsd_fit_recovers_reference_after_rigid_transform(float64_kernel_atol):
    """Recover an asymmetric reference exactly after rotation and translation."""

    reference = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.2, 1.3, 0.0], [0.1, 0.2, 0.9]]
    )
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    transformed = reference @ rotation.T + np.array([2.0, -3.0, 0.5])
    system = Structures(
        coordinates=np.stack([reference, transformed]) * msm.pyunitwizard.unit("nm")
    )

    fitted = msm.structure.least_rmsd_fit(
        system,
        selection="all",
        selection_fit="all",
        reference_structure_index=0,
        in_place=False,
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(fitted.coordinates, to_unit="nm")

    np.testing.assert_allclose(
        observed,
        np.stack([reference, reference]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
