"""Analytic scientific truth tests for ensemble structural observables."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import Structures


def _structures(coordinates_nm):
    return Structures(coordinates=coordinates_nm * msm.pyunitwizard.unit("nm"))


def _values(quantity):
    return msm.pyunitwizard.get_value(quantity, to_unit="nm")


def test_geometric_and_weighted_centers_match_closed_form(float64_kernel_atol):
    """Validate centroids and weighted centers against explicit sums."""

    coordinates = np.array(
        [[[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 3.0, 0.0]]],
        dtype=np.float64,
    )
    system = _structures(coordinates)

    geometric = msm.structure.get_center(system, selection="all", heavy_mode="off")
    weighted = msm.structure.get_center(
        system,
        selection="all",
        weights=np.array([1.0, 2.0, 3.0]),
        heavy_mode="off",
    )

    np.testing.assert_allclose(
        _values(geometric),
        np.array([[[2.0 / 3.0, 1.0, 0.0]]]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _values(weighted),
        np.array([[[2.0 / 3.0, 1.5, 0.0]]]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_radius_of_gyration_matches_closed_form_and_rigid_invariance(float64_kernel_atol):
    """Validate Rg for three collinear points and a rigidly transformed copy."""

    reference = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    transformed = reference @ rotation.T + np.array([4.0, -2.0, 0.5])
    observed = msm.structure.get_radius_of_gyration(
        _structures(np.stack([reference, transformed])),
        selection="all",
        heavy_mode="off",
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _values(observed),
        np.full(2, np.sqrt(2.0 / 3.0)),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_weighted_radius_of_gyration_matches_closed_form(float64_kernel_atol):
    """Validate weighted Rg using an independently expanded scalar formula."""

    coordinates = np.array([[[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]]])
    weights = np.array([1.0, 3.0])
    observed = msm.structure.get_radius_of_gyration(
        _structures(coordinates),
        selection="all",
        weights=weights,
        heavy_mode="off",
        use_gpu=False,
    )

    # Weighted center = 1.5 nm; Rg^2 = (1*1.5^2 + 3*0.5^2) / 4.
    expected = np.sqrt(0.75)
    np.testing.assert_allclose(
        _values(observed),
        np.array([expected]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_rmsf_matches_closed_form_and_common_rigid_invariance(float64_kernel_atol):
    """Validate RMSF and invariance under one common rigid transformation."""

    coordinates = np.array(
        [
            [[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
            [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
        ]
    )
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    transformed = coordinates @ rotation.T + np.array([3.0, -4.0, 2.0])

    observed = msm.structure.get_rmsf(
        _structures(coordinates), selection="all", heavy_mode="off"
    )
    transformed_observed = msm.structure.get_rmsf(
        _structures(transformed), selection="all", heavy_mode="off"
    )

    expected = np.array([1.0, 1.0])
    np.testing.assert_allclose(
        _values(observed), expected, rtol=0.0, atol=float64_kernel_atol
    )
    np.testing.assert_allclose(
        _values(transformed_observed), expected, rtol=0.0, atol=float64_kernel_atol
    )


@pytest.mark.parametrize("function_name", ["get_center", "get_radius_of_gyration"])
def test_weighted_observables_reject_zero_total_weight(function_name):
    """Reject the undefined zero-total-weight degeneracy at the public boundary."""

    system = _structures(np.zeros((1, 2, 3), dtype=np.float64))
    function = getattr(msm.structure, function_name)

    with pytest.raises(ArgumentError):
        function(system, selection="all", weights=np.zeros(2), heavy_mode="off")


def test_single_atom_and_single_frame_degenerate_limits(float64_kernel_atol):
    """Validate the exact zero limits of Rg and RMSF."""

    system = _structures(np.array([[[2.0, -1.0, 4.0]]]))
    rg = msm.structure.get_radius_of_gyration(
        system, selection="all", heavy_mode="off", use_gpu=False
    )
    rmsf = msm.structure.get_rmsf(system, selection="all", heavy_mode="off")

    np.testing.assert_allclose(_values(rg), 0.0, rtol=0.0, atol=float64_kernel_atol)
    np.testing.assert_allclose(_values(rmsf), 0.0, rtol=0.0, atol=float64_kernel_atol)


@pytest.mark.parametrize(
    "function_name", ["get_center", "get_radius_of_gyration", "get_rmsf"]
)
def test_ensemble_reductions_reject_empty_frame_selections(function_name):
    """Reject reductions over zero structures instead of returning NaN or crashing."""

    system = _structures(np.zeros((2, 2, 3), dtype=np.float64))
    function = getattr(msm.structure, function_name)

    with pytest.raises(ArgumentError):
        function(system, selection="all", structure_indices=[], heavy_mode="off")
