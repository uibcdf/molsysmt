"""Preserve physical reference origins under presentation-unit changes (#608)."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("sign", [-1, 0, 1])
@pytest.mark.parametrize("mode", ["primary", "centered", "mic"])
@pytest.mark.parametrize("compact", [False, "component"])
@pytest.mark.parametrize("in_place", [False, True])
def test_small_explicit_origins_do_not_change_the_physical_periodic_image(
    unit, sign, mode, compact, in_place
):
    origin = np.array([sign * 1e-5, 0.0, 0.0])
    center = origin[0] / 2 + (0 if mode == "primary" else 1.5)
    row = (
        [[center - 0.01, 0, 0], [center + 0.01, 0, 0]]
        if compact
        else [[center, 0, 0], [center + origin[0] / 4, 0, 0]]
    )
    coordinates = np.repeat(np.array([row]), 3, axis=0)
    coordinates[:, :, 1] += np.arange(3)[:, None] / 10
    source = MolSys(n_atoms=2)
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    source.structures.box = puw.quantity(
        np.repeat(np.diag([3.0, 4, 5])[None], 3, axis=0), "nm"
    )
    source.chemical_states.add_bonds([[0, 1]])
    expected = coordinates.copy()
    if compact:
        shift = (
            np.floor((center - origin[0]) / 3 + (0 if mode == "primary" else 0.5)) * 3
        )
        expected[[2, 0], :, 0] -= shift
    else:
        expected[[2, 0], :, 0] -= (
            np.floor(
                (coordinates[[2, 0], :, 0] - origin[0]) / 3
                + (0 if mode == "primary" else 0.5)
            )
            * 3
        )
    with puw.context(standard_units=[unit, "ps"]):
        supplied = puw.convert(puw.quantity(origin, "nm"), to_unit="angstrom")
        before = puw.get_value(supplied).copy()
        if mode == "mic":
            returned = msm.pbc.wrap_to_mic(
                source,
                mic_origin=supplied,
                compact=compact,
                in_place=in_place,
                structure_indices=[2, 0],
            )
        else:
            keyword = "box_origin" if mode == "primary" else "box_center"
            returned = msm.pbc.wrap_to_pbc(
                source,
                compact=compact,
                in_place=in_place,
                structure_indices=[2, 0],
                **{keyword: supplied},
            )
        np.testing.assert_array_equal(puw.get_value(supplied), before)
    result = source if in_place else returned
    assert (returned is None) == in_place
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        expected,
        rtol=0,
        atol=1e-11,
    )
    if not in_place:
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit="nm"), coordinates
        )


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm", "m"])
@pytest.mark.parametrize("operation", ["primary", "mic", "unwrap"])
@pytest.mark.parametrize("edge_nm", [1e-6, 3.0])
@pytest.mark.parametrize("left_handed", [False, True])
def test_box_nonsingularity_admission_is_invariant_under_length_units(
    unit, operation, edge_nm, left_handed
):
    source = MolSys(n_atoms=1)
    coordinates = np.array([[[0.9, 0, 0]], [[0.1, 0, 0]]]) * edge_nm
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    box = np.eye(3) * edge_nm
    if left_handed:
        box[0] *= -1
    source.structures.box = puw.quantity(np.repeat(box[None], 2, axis=0), "nm")
    with puw.context(standard_units=[unit, "ps"]):
        if operation == "unwrap":
            result = msm.pbc.unwrap(source)
            expected = [0.9, 1.1]
        else:
            result = _wrap_small(source, operation)
            expected = (
                ([-0.1, -0.9] if left_handed else [0.9, 0.1])
                if operation == "primary"
                else [-0.1, 0.1]
            )
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm")[:, 0, 0],
        np.array(expected) * edge_nm,
        rtol=0,
        atol=edge_nm * 1e-12,
    )


def _wrap_small(source, mode):
    if mode == "mic":
        return msm.pbc.wrap_to_mic(source, compact=False)
    return msm.pbc.wrap_to_pbc(source, compact=False)
