"""Check native Simulation parameter handling and missing-system errors."""

import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import MolecularSystemNeededError
from molsysmt.native import Simulation


def test_set_parameters_updates_known_values_and_returns_unknown_ones():
    """A processed parameter is removed from the remaining keyword arguments."""
    simulation = Simulation()

    remaining = simulation.set_parameters(
        return_non_processed=True, TEMPERATURE="300 K", mystery="unchanged"
    )

    assert remaining == {"mystery": "unchanged"}
    assert puw.get_value(simulation.temperature, to_unit="K") == 300


@pytest.mark.parametrize("method", ["to_openmm_Context", "to_openmm_Simulation"])
def test_conversion_requires_a_molecular_system(method):
    """Both conversion methods report the missing native input explicitly."""
    simulation = Simulation()

    with pytest.raises(MolecularSystemNeededError):
        getattr(simulation, method)()
