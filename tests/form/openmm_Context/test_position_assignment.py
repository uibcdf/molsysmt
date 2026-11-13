"""Keep mutable Context assignment distinct from immutable State refusal."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("element", ["atom", "system"])
@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_public_context_coordinate_assignment_accepts_shared_structure_selector(
    openmm_reference_context, element, length, time
):
    from openmm import unit

    source = openmm_reference_context
    arguments = {"selection": [1]} if element == "atom" else {}
    requested = [[[4, 5, 6]]] if element == "atom" else [[[4, 5, 6], [7, 8, 9]]]
    expected = [[0, 0, 0], [4, 5, 6]] if element == "atom" else requested[0]
    with puw.context(standard_units=[length, time, "radians"]):
        msm.set(
            source,
            element=element,
            structure_indices=[0],
            coordinates=puw.quantity(requested, "nm"),
            **arguments,
        )
        positions = source.getState(getPositions=True).getPositions(asNumpy=True)
        np.testing.assert_allclose(
            positions.value_in_unit(unit.nanometer), expected, rtol=0, atol=1e-12
        )
