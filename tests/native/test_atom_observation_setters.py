"""Assign optional atom observations without losing fractions or copying geometry."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures
from molsysmt.native._structure_array import _StructureArray


@pytest.mark.parametrize(
    "name,value",
    [
        ("occupancy", np.array([[0.5]])),
        ("b_factor", msm.pyunitwizard.quantity([[24.0]], "angstrom**2")),
    ],
)
def test_first_selected_assignment_does_not_materialize_coordinates(
    monkeypatch, name, value
):
    item = Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((3, 4, 3)), "nm"))
    coordinates = item._coordinates

    def forbidden(*args, **kwargs):
        raise AssertionError("Observation allocation must use the stored axis shapes.")

    monkeypatch.setattr(_StructureArray, "_dense", forbidden)
    getattr(item, "set_" + name)(indices=[1], structure_indices=[2], value=value)
    result = getattr(item, name)
    if name == "b_factor":
        result = msm.pyunitwizard.get_value(result, to_unit="nm**2")
    assert result.shape == (3, 4)
    assert result[2, 1] == pytest.approx(0.5 if name == "occupancy" else 0.24)
    assert np.isnan(result[0, 0])
    assert item._coordinates is coordinates


@pytest.mark.parametrize("name", ["occupancy", "b_factor"])
def test_rejected_first_subset_keeps_optional_observation_absent(name):
    item = Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm"))
    value = np.array([[0.25]])
    if name == "b_factor":
        value = msm.pyunitwizard.quantity(value, "nm**2")
    with pytest.raises(IndexError):
        getattr(item, "set_" + name)(indices=[10], structure_indices=[0], value=value)
    assert getattr(item, name) is None
