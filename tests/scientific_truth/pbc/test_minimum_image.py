"""Analytic truth tests for minimum-image distances."""

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def _distance_values(structures):
    distances = msm.structure.get_distances(
        structures,
        selection=[0],
        selection_2=[1],
        pbc=True,
        use_gpu=False,
    )
    return msm.pyunitwizard.get_value(distances, to_unit="nm")


def test_orthorhombic_minimum_image_distance_is_point_two_nm(float64_kernel_atol):
    """Validate points at x=0.1 and 1.9 nm in a 2 nm periodic cell."""

    unit = msm.pyunitwizard.unit("nm")
    structures = Structures(
        coordinates=np.array([[[0.1, 0.0, 0.0], [1.9, 0.0, 0.0]]]) * unit,
        box=np.array([np.diag([2.0, 2.0, 2.0])]) * unit,
    )

    np.testing.assert_allclose(
        _distance_values(structures),
        [[[0.2]]],
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_triclinic_minimum_image_matches_fractional_coordinate_truth(float64_kernel_atol):
    """Validate a fractional displacement of (-0.1, -0.1, 0) in a 60-degree cell."""

    unit = msm.pyunitwizard.unit("nm")
    box = np.array(
        [[2.0, 0.0, 0.0], [1.0, np.sqrt(3.0), 0.0], [0.0, 0.0, 3.0]]
    )
    fractional = np.array([[0.05, 0.05, 0.0], [0.95, 0.95, 0.0]])
    coordinates = fractional @ box
    structures = Structures(
        coordinates=coordinates[None, :, :] * unit,
        box=box[None, :, :] * unit,
    )

    np.testing.assert_allclose(
        _distance_values(structures),
        [[[np.sqrt(0.12)]]],
        rtol=0.0,
        atol=float64_kernel_atol,
    )
