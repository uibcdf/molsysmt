"""Protecting generic dispatch to native mechanical atom-index setters."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolecularMechanics


@pytest.mark.parametrize("selection", ["all", [2, 0]])
@pytest.mark.parametrize(
    "attribute,initial,new",
    [
        ("atom_ff_type", ["C", "N", "OA"], ["A", "NA", "O"]),
        ("partial_charge", [0.1, 0.2, -0.3], [0.5, 0.0, -0.5]),
    ],
)
def test_generic_setter_preserves_native_adapter_atom_index_contract(
    selection, attribute, initial, new
):
    mechanics = MolecularMechanics(**{attribute: initial})
    values = new if selection == "all" else new[:2]
    msm.set(mechanics, element="atom", selection=selection, **{attribute: values})
    expected = new if selection == "all" else [new[1], initial[1], new[0]]
    np.testing.assert_array_equal(getattr(mechanics, attribute), expected)


@pytest.mark.parametrize("value", [["C"], [1, 2], [["C", "N"]]])
def test_invalid_label_vectors_do_not_mutate_mechanical_storage(value):
    from molsysmt._private.smonitor import ArgumentError

    mechanics = MolecularMechanics(atom_ff_type=["C", "N"])
    before = mechanics.atoms_ff.copy()
    with pytest.raises(ArgumentError):
        msm.set(mechanics, element="atom", atom_ff_type=value)
    assert mechanics.atoms_ff.equals(before)
