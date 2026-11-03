"""Reject boolean structure positions at the shared public digestion boundary."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolSys, Structures


@pytest.mark.parametrize(
    "indices", [True, np.bool_(False), [True], [0, True], (False, 1)]
)
@pytest.mark.parametrize("tool", ["get", "select", "convert"])
def test_boolean_values_cannot_become_integer_structure_indices(indices, tool):
    source = MolSys(n_atoms=1)
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 1, 3)), "nm")
    )
    options = (
        {"coordinates": True}
        if tool == "get"
        else (
            {"to_form": "molsysmt.Structures"}
            if tool == "convert"
            else {"selection": "atom_index == 0"}
        )
    )
    with pytest.raises(ArgumentError, match="structure_indices"):
        getattr(msm, tool)(source, structure_indices=indices, **options)
