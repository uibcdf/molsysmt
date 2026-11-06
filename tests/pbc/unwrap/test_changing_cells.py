"""Use the actual previous structure cell for each unwrap transition (#606)."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys
from tests.pbc.test_general_cell_wrapping import _minimum_image


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("triclinic_first", [False, True])
def test_unwrap_reclassifies_each_previous_transition_cell(
    in_place, unit, triclinic_first
):
    orthogonal = np.diag([3.0, 4, 5])
    triclinic = np.array([[3.0, 0, 0], [2, 4, 0], [0, 0, 5]])
    boxes = np.array([orthogonal, triclinic, triclinic])
    coordinates = np.array([[[0.0, 0, 0]], [[0.0, 0, 0]], [[1.9, 3.8, 0]]])
    if triclinic_first:
        # Both transitions must actually use different classifications. Reversing
        # [orthogonal, triclinic, triclinic] would use triclinic twice instead.
        boxes = np.array([triclinic, orthogonal, orthogonal])
    source = MolSys(n_atoms=1)
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    source.structures.box = puw.quantity(boxes, "nm")
    expected = coordinates.copy()
    for i in range(2):
        expected[i + 1, 0] = expected[i, 0] + _minimum_image(
            coordinates[i + 1, 0] - expected[i, 0], boxes[i]
        )

    with puw.context(standard_units=[unit, "ps"]):
        returned = msm.pbc.unwrap(source, in_place=in_place)
    result = source if in_place else returned
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        expected,
        rtol=0,
        atol=1e-12,
    )
    if not in_place:
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit="nm"), coordinates
        )


@pytest.mark.parametrize("order", [[0, 2], [2, 0]])
def test_unwrap_uses_previous_cell_in_requested_structure_order(order):
    boxes = np.array([np.diag([2.0, 3, 4]), np.diag([4.0, 3, 4]), np.diag([8.0, 3, 4])])
    coordinates = np.array([[[0.0, 0, 0]], [[1.2, 0, 0]], [[3.4, 0, 0]]])
    source = MolSys(n_atoms=1)
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    source.structures.box = puw.quantity(boxes, "nm")
    result = msm.pbc.unwrap(source, structure_indices=order)
    expected = coordinates.copy()
    if order == [0, 2]:
        # Displacement 3.4 uses the previous 2 nm cell -> -0.6.
        expected[2, 0, 0] = -0.6
    # Traversal [2, 0] instead uses the previous 8 nm cell: no image shift.
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        expected,
        rtol=0,
        atol=1e-12,
    )


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("rotated", [False, True])
@pytest.mark.parametrize(
    "jump,expected_fraction", [(0.5, 0.5), (1.5, -0.5), (-0.5, -0.5), (-1.5, 0.5)]
)
def test_unwrap_preserves_actual_half_cell_ties_to_even(
    unit, rotated, jump, expected_fraction
):
    box = (
        np.array([[0.0, 3, 0], [-4, 0, 0], [0, 0, 5]])
        if rotated
        else np.diag([3.0, 4, 5])
    )
    coordinates = np.array([[np.zeros(3)], [jump * box[0]]])
    source = MolSys(n_atoms=1)
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    source.structures.box = puw.quantity(np.repeat(box[None], 2, axis=0), "nm")
    with puw.context(standard_units=[unit, "ps"]):
        result = msm.pbc.unwrap(source)
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm")[1, 0],
        expected_fraction * box[0],
        rtol=0,
        atol=1e-12,
    )
