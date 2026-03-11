import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.atom_id import digest_atom_id
from molsysmt._private.arg_digestion.argument.group_id import digest_group_id
from molsysmt._private.arg_digestion.argument.chain_id import digest_chain_id
from molsysmt._private.arg_digestion.argument.molecule_id import digest_molecule_id
from molsysmt._private.arg_digestion.argument.entity_id import digest_entity_id
from molsysmt._private.arg_digestion.argument.component_id import digest_component_id
from molsysmt._private.arg_digestion.argument.atom_index import digest_atom_index
from molsysmt._private.arg_digestion.argument.group_index import digest_group_index
from molsysmt._private.arg_digestion.argument.chain_index import digest_chain_index
from molsysmt._private.arg_digestion.argument.molecule_index import digest_molecule_index
from molsysmt._private.arg_digestion.argument.entity_index import digest_entity_index
from molsysmt._private.arg_digestion.argument.component_index import digest_component_index
from molsysmt._private.arg_digestion.argument.n_atoms import digest_n_atoms
from molsysmt._private.arg_digestion.argument.n_groups import digest_n_groups
from molsysmt._private.arg_digestion.argument.n_chains import digest_n_chains
from molsysmt._private.arg_digestion.argument.n_components import digest_n_components
from molsysmt._private.arg_digestion.argument.n_molecules import digest_n_molecules
from molsysmt._private.arg_digestion.argument.n_entities import digest_n_entities

GET_CALLER = "molsysmt.basic.get.get"
COMPARE_CALLER = "molsysmt.basic.compare.compare"
NATIVE_TOPOLOGY_CALLER = "molsysmt.native.topology.__init__"
NATIVE_MOLSYS_CALLER = "molsysmt.native.molsys.__init__"


def test_id_digesters_support_builder_callers_and_boolean_queries():
    assert digest_atom_id(None, caller='molsysmt.native.molsys_builder.MolSysBuilder.add_atom') is None
    assert digest_group_id(None, caller='molsysmt.native.molsys_builder.MolSysBuilder.add_group') is None
    assert digest_chain_id(None, caller='molsysmt.native.molsys_builder.MolSysBuilder.add_chain') is None
    assert digest_chain_id(None, caller='molsysmt.native.molsys_builder.MolSysBuilder.assign_groups_to_new_chain') is None
    assert digest_molecule_id(None, caller='molsysmt.native.molsys_builder.MolSysBuilder.add_molecule') is None
    assert digest_entity_id(None, caller='molsysmt.native.molsys_builder.MolSysBuilder.add_entity') is None

    assert digest_atom_id(True, caller=GET_CALLER) is True
    assert digest_group_id(False, caller=COMPARE_CALLER) is False
    assert digest_chain_id(True, caller=GET_CALLER) is True
    assert digest_molecule_id(False, caller=COMPARE_CALLER) is False
    assert digest_entity_id(True, caller=GET_CALLER) is True
    assert digest_component_id(True, caller=GET_CALLER) is True


def test_id_digesters_normalize_scalars_and_lists():
    assert digest_atom_id(7, caller='molsysmt.native.molsys_builder.MolSysBuilder.add_atom') == 7
    assert digest_group_id('A', caller='molsysmt.native.molsys_builder.MolSysBuilder.add_group') == 'A'
    assert digest_chain_id(2, caller='molsysmt.native.molsys_builder.MolSysBuilder.add_chain') == 2
    assert digest_molecule_id('mol', caller='molsysmt.native.molsys_builder.MolSysBuilder.add_molecule') == 'mol'
    assert digest_entity_id('ent', caller='molsysmt.native.molsys_builder.MolSysBuilder.add_entity') == 'ent'

    assert digest_component_id(3) == [3]
    assert digest_component_id([1, 2]) == [1, 2]
    assert digest_component_id('all') == 'all'


def test_index_digesters_support_boolean_queries_and_normalize_values():
    assert digest_atom_index(True, caller=GET_CALLER) is True
    assert digest_group_index(False, caller=COMPARE_CALLER) is False
    assert digest_chain_index(True, caller=GET_CALLER) is True
    assert digest_molecule_index(False, caller=COMPARE_CALLER) is False
    assert digest_entity_index(True, caller=GET_CALLER) is True
    assert digest_component_index(False, caller=COMPARE_CALLER) is False

    assert digest_atom_index(3) == [3]
    assert digest_group_index([1, 2]) == [1, 2]
    assert digest_chain_index('all') == 'all'
    assert digest_molecule_index(4) == [4]
    assert digest_entity_index([0, 1]) == [0, 1]
    assert digest_component_index(2) == [2]


def test_count_digesters_support_boolean_and_native_constructor_ints():
    assert digest_n_atoms(True, caller=GET_CALLER) is True
    assert digest_n_groups(False, caller=COMPARE_CALLER) is False
    assert digest_n_chains(True, caller=GET_CALLER) is True
    assert digest_n_components(False, caller=COMPARE_CALLER) is False
    assert digest_n_molecules(True, caller=GET_CALLER) is True
    assert digest_n_entities(False, caller=COMPARE_CALLER) is False

    assert digest_n_atoms(3, caller=NATIVE_TOPOLOGY_CALLER) == 3
    assert digest_n_groups(2, caller=NATIVE_MOLSYS_CALLER) == 2
    assert digest_n_chains(1, caller=NATIVE_TOPOLOGY_CALLER) == 1
    assert digest_n_components(4, caller=NATIVE_MOLSYS_CALLER) == 4
    assert digest_n_molecules(5, caller=NATIVE_TOPOLOGY_CALLER) == 5
    assert digest_n_entities(6, caller=NATIVE_MOLSYS_CALLER) == 6


def test_index_and_count_digesters_reject_invalid_inputs():
    with pytest.raises(ArgumentError):
        digest_atom_index('CA')
    with pytest.raises(ArgumentError):
        digest_component_index({'a': 1})
    with pytest.raises(ArgumentError):
        digest_n_atoms('3', caller=NATIVE_TOPOLOGY_CALLER)
    with pytest.raises(ArgumentError):
        digest_n_groups('2', caller=NATIVE_MOLSYS_CALLER)
