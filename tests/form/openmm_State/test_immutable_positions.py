"""Refuse unsupported State mutation without changing captured positions."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import NotImplementedMethodError


@pytest.mark.parametrize("element", ["atom", "system"])
@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_public_coordinate_assignment_refuses_a_captured_state(
    openmm_position_snapshot, element, length, time
):
    from openmm import unit

    source = openmm_position_snapshot
    before = source.getPositions(asNumpy=True).value_in_unit(unit.nanometer).copy()
    with puw.context(standard_units=[length, time, "radians"]):
        with pytest.raises(NotImplementedMethodError):
            msm.set(
                source,
                element=element,
                coordinates=puw.quantity([[[4, 5, 6], [7, 8, 9]]], "nm"),
            )
    np.testing.assert_array_equal(
        source.getPositions(asNumpy=True).value_in_unit(unit.nanometer), before
    )


@pytest.mark.parametrize("element", ["atom", "system"])
def test_direct_adapter_refuses_instead_of_calling_a_missing_state_mutator(
    openmm_position_snapshot, element
):
    from molsysmt.form.openmm_State.set import (
        set_coordinates_to_atom,
        set_coordinates_to_system,
    )

    function = (
        set_coordinates_to_atom if element == "atom" else set_coordinates_to_system
    )
    with pytest.raises(NotImplementedMethodError):
        function(
            openmm_position_snapshot,
            value=puw.quantity([[[4, 5, 6], [7, 8, 9]]], "nm"),
        )
