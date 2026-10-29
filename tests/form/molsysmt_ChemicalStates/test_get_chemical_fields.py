"""Check direct form delivery as well as native and universal query clients."""

import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt.form import molsysmt_ChemicalStates as adapter
from tests.native import test_chemical_state_field_queries as fixtures

fields = fixtures.fields


@pytest.mark.parametrize(
    "getter,indices,expected",
    [
        ("get_formal_charge_from_atom", [2, 1], [-1, None]),
        ("get_atom_is_aromatic_from_atom", [0, 2], [False, True]),
        ("get_bond_order_from_bond", [1, 0, 1], [0, 1, 0]),
        ("get_bond_stereo_atom_indices_from_bond", [1], [[1, 2]]),
        ("get_component_id_from_atom", [1, 2], [None, "last"]),
        ("get_component_type_from_component", [1, 0], ["small molecule", None]),
    ],
)
def test_direct_getters_deliver_declared_nullable_fields(
    fields, getter, indices, expected
):
    assert getattr(adapter, getter)(fields, indices=indices) == expected


@pytest.mark.parametrize(
    "getter,indices",
    [
        ("get_formal_charge_from_atom", [3]),
        ("get_bond_order_from_bond", [-1]),
        ("get_component_id_from_component", [2]),
    ],
)
def test_direct_getters_reject_out_of_domain_positions(fields, getter, indices):
    with pytest.raises(ArgumentError):
        getattr(adapter, getter)(fields, indices=indices)
