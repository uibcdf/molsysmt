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


@pytest.mark.parametrize(
    "setter,getter,value,expected",
    [
        ("set_formal_charge_to_atom", "get_formal_charge_from_atom", 2, 2),
        ("set_atom_is_aromatic_to_atom", "get_atom_is_aromatic_from_atom", None, None),
        ("set_bond_id_to_bond", "get_bond_id_from_bond", 42, "42"),
        ("set_bond_order_to_bond", "get_bond_order_from_bond", 2, 2),
    ],
)
def test_direct_setters_use_selected_positions_and_nullable_values(
    fields, setter, getter, value, expected
):
    getattr(adapter, setter)(fields, indices=[0], value=value)
    assert getattr(adapter, getter)(fields, indices=[0]) == [expected]


def test_explicitly_trusted_assignment_still_rejects_unrepresentable_storage(fields):
    from molsysmt._private.smonitor import StructuralInconsistencyError

    before = fields._states[0].atom_attributes
    with pytest.raises(StructuralInconsistencyError):
        adapter.set_formal_charge_to_atom(
            fields, indices=[0], value=40000, skip_digestion=True
        )
    assert fields._states[0].atom_attributes is before
