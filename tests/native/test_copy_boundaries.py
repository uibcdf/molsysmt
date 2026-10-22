"""Copy boundaries retain table identity and slot ownership without losing data."""

import copy
import pickle

import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt.native import ChemicalStates, MolSys, Structures, Topology
from tests.native.test_molsys_copy import _copy_system
from tests.native.test_molsys_interactions import _analysis, _system

OPERATIONS = (copy.copy, copy.deepcopy, lambda value: value.copy())


@pytest.fixture
def molecular_system():
    return _copy_system()


class SlottedTopologyOwner(Topology):
    __slots__ = ("_molsys_owner_ref",)


class SlottedStatesOwner(ChemicalStates):
    __slots__ = ("_molsys_owner_ref",)


class SlottedStructuresOwner(Structures):
    __slots__ = ("_molsys_owner_ref",)


@pytest.fixture(
    params=[
        ("topology", SlottedTopologyOwner),
        ("chemical_states", SlottedStatesOwner),
        ("structures", SlottedStructuresOwner),
    ]
)
def slotted_system(request):
    name, cls = request.param
    system = _system()
    if name == "structures":
        domain = cls(coordinates=puw.quantity(np.zeros((3, 3, 3)), "nm"))
    else:
        domain = cls(n_atoms=3)
        if name == "chemical_states":
            domain.append_state()
    setattr(system, name, domain)
    system.interactions = {"pairs": _analysis()}
    return system, name


@pytest.mark.parametrize("operation", OPERATIONS)
def test_standalone_domain_copies_detach_owners_stored_in_slots(
    slotted_system, operation
):
    system, name = slotted_system
    domain = getattr(system, name)
    duplicate = operation(domain)
    assert getattr(duplicate, "_molsys_owner_ref", None) is None
    assert domain._molsys_owner_ref() is system
    original_analysis = system.interactions["pairs"]
    if name == "structures":
        duplicate.set_coordinates(
            indices=[0],
            structure_indices=[0],
            value=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
        )
        np.testing.assert_array_equal(puw.get_value(domain.coordinates), 0.0)
    elif name == "chemical_states":
        duplicate.append_state()
        assert domain.n_chemical_states == 1
    else:
        duplicate.add_bonds([[0, 1]])
        assert domain.n_bonds == 0
    assert system.interactions["pairs"] is original_analysis
    np.testing.assert_array_equal(
        original_analysis.evaluated_structure_indices, [0, 1, 2]
    )


@pytest.mark.parametrize("operation", OPERATIONS)
def test_whole_system_copy_rebinds_owners_stored_in_domain_slots(
    slotted_system, operation
):
    system, name = slotted_system
    duplicate = operation(system)
    assert getattr(duplicate, name)._molsys_owner_ref() is duplicate
    assert getattr(system, name)._molsys_owner_ref() is system
    if name == "structures":
        duplicate.structures.set_coordinates(
            indices=[0],
            structure_indices=[0],
            value=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
        )
        np.testing.assert_array_equal(
            duplicate.interactions["pairs"].evaluated_structure_indices, [1, 2]
        )
    elif name == "chemical_states":
        duplicate.chemical_states.append_state()
        assert duplicate.interactions["pairs"].evaluated_structure_indices.size == 0
    else:
        duplicate.topology.add_bonds([[0, 1]])
        assert duplicate.interactions["pairs"].evaluated_structure_indices.size == 0
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [0, 1, 2]
    )


@pytest.mark.parametrize("base", [Topology, ChemicalStates, MolSys, Structures])
@pytest.mark.parametrize("operation", OPERATIONS)
def test_shadowed_slot_records_keep_distinct_values_and_graph_aliases(base, operation):
    class Parent(base):
        __slots__ = ("payload",)

    class Child(Parent):
        __slots__ = ("payload",)

    source = Child()
    first = {"owner": source, "values": [1]}
    second = {"owner": source, "values": [2]}
    Parent.payload.__set__(source, first)
    Child.payload.__set__(source, second)
    source.base_alias = first
    source.child_alias = second
    duplicate = operation(source)
    copied_first = Parent.payload.__get__(duplicate)
    copied_second = Child.payload.__get__(duplicate)
    assert copied_first is duplicate.base_alias
    assert copied_second is duplicate.child_alias
    assert copied_first is not copied_second
    assert copied_first["owner"] is copied_second["owner"] is duplicate
    copied_first["values"].append(3)
    copied_second["values"].append(4)
    assert first["values"] == [1]
    assert second["values"] == [2]


@pytest.mark.parametrize("operation", OPERATIONS)
def test_slots_declared_by_an_exhausted_iterator_are_not_lost(operation):
    class Extended(Topology):
        __slots__ = iter(("payload", "__secret", "unset"))

    source = Extended(n_atoms=2)
    source.payload = {"values": [1], "owner": source}
    source._Extended__secret = source.payload
    duplicate = operation(source)
    assert duplicate.payload is duplicate._Extended__secret
    assert duplicate.payload["owner"] is duplicate
    assert not hasattr(duplicate, "unset")
    duplicate.payload["values"].append(2)
    assert source.payload["values"] == [1]


@pytest.mark.parametrize("order", ["system_first", "table_first"])
def test_canonical_table_aliases_follow_the_containing_graph_memo(
    molecular_system, order
):
    source = molecular_system
    tables = [
        source.topology.atoms,
        source.topology.groups,
        source.chemical_states._states[0].bonds,
        source.chemical_states._states[0].atom_attributes,
        source.molecular_mechanics.atoms_ff,
    ]
    source.table_aliases = tables
    graph = [source, tables] if order == "system_first" else [tables, source]
    result = copy.deepcopy(graph)
    duplicate, aliases = result if order == "system_first" else result[::-1]
    actual = [
        duplicate.topology.atoms,
        duplicate.topology.groups,
        duplicate.chemical_states._states[0].bonds,
        duplicate.chemical_states._states[0].atom_attributes,
        duplicate.molecular_mechanics.atoms_ff,
    ]
    assert aliases is duplicate.table_aliases
    assert all(alias is table for alias, table in zip(aliases, actual))
    assert all(table is not original for table, original in zip(actual, tables))
    actual[0].at[0, "atom_name"] = "changed"
    assert tables[0].at[0, "atom_name"] != "changed"


class StateParent(ChemicalStates):
    __slots__ = ("payload",)


class StateChild(StateParent):
    __slots__ = ("payload",)


@pytest.mark.parametrize("stored", ["both", "parent", "child"])
def test_pickle_rejects_ambiguous_slot_names_instead_of_dropping_a_state_value(stored):
    source = StateChild(n_atoms=2)
    if stored in {"both", "parent"}:
        StateParent.payload.__set__(source, {"values": [1]})
    if stored in {"both", "child"}:
        StateChild.payload.__set__(source, {"values": [2]})
    with pytest.raises(TypeError, match="slot.*payload"):
        pickle.dumps(source)
    duplicate = copy.deepcopy(source)
    for descriptor, index, active in [
        (StateParent.payload, 1, {"both", "parent"}),
        (StateChild.payload, 2, {"both", "child"}),
    ]:
        if stored in active:
            assert descriptor.__get__(source) == {"values": [index]}
            assert descriptor.__get__(duplicate) == {"values": [index]}
            assert descriptor.__get__(source) is not descriptor.__get__(duplicate)
        else:
            with pytest.raises(AttributeError):
                descriptor.__get__(duplicate)


@pytest.mark.parametrize("operation", OPERATIONS)
def test_live_resource_failure_does_not_transfer_the_source_owner(
    molecular_system, operation, tmp_path
):
    source = molecular_system
    with (tmp_path / "resource.bin").open("wb") as resource:
        source.resource = resource
        previous = dict(source.interactions)
        with pytest.raises(TypeError):
            operation(source)
        assert source.topology._molsys_owner_ref() is source
        assert source.chemical_states._molsys_owner_ref() is source
        assert not resource.closed
        assert all(
            source.interactions[name] is value for name, value in previous.items()
        )
