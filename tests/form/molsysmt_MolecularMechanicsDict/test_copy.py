"""Universal copying detaches plain mechanical parameter dictionaries."""

import copy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form.molsysmt_MolecularMechanicsDict.copy import copy as copy_parameters


@pytest.mark.parametrize("operation", [msm.copy, copy_parameters])
def test_parameter_copy_detaches_nested_values_and_preserves_units(operation):
    source = {
        "forcefield": ["amber14-all.xml"],
        "partial_charge": np.array([0.1, -0.1]),
        "cutoff_distance": puw.quantity(1.0, "nm"),
    }
    duplicate = operation(source)
    duplicate["forcefield"].append("amber14/tip3p.xml")
    duplicate["partial_charge"][0] = 0.9
    assert source["forcefield"] == ["amber14-all.xml"]
    np.testing.assert_array_equal(source["partial_charge"], [0.1, -0.1])
    assert puw.get_value(duplicate["cutoff_distance"], to_unit="nm") == 1.0
    assert copy.copy(source)["forcefield"] is source["forcefield"]
