import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.attribute_type import digest_attribute_type
from molsysmt._private.argdigest.argument.indices import digest_indices
from molsysmt._private.argdigest.argument.item import digest_item
from molsysmt._private.argdigest.argument.items import digest_items
from molsysmt._private.argdigest.argument.keys import digest_keys
from molsysmt.native.topology import Topology
from molsysmt.native.molsys import MolSys


def test_digest_attribute_type_accepts_supported_values():
    assert digest_attribute_type(None, caller='molsysmt.basic.compare.compare') is None
    assert digest_attribute_type('all', caller='molsysmt.basic.compare.compare') == 'all'
    assert digest_attribute_type('Topological', caller='molsysmt.basic.compare.compare') == 'topological'
    assert digest_attribute_type('structural', caller='molsysmt.basic.get_attributes.get_attributes') == 'structural'
    assert digest_attribute_type('mechanical', caller='molsysmt.basic.get_attributes.get_attributes') == 'mechanical'
    with pytest.raises(ArgumentError):
        digest_attribute_type('bad', caller='molsysmt.basic.compare.compare')


def test_digest_indices_accepts_common_iterables():
    assert digest_indices(None) is None
    assert digest_indices('all') == 'all'
    assert digest_indices(3) == [3]
    assert digest_indices(range(3)) == [0, 1, 2]
    assert digest_indices((0, 2)) == [0, 2]
    assert digest_indices([1, 4]) == [1, 4]
    with pytest.raises(ArgumentError):
        digest_indices({'bad': 1})


def test_digest_item_accepts_items_and_form_checks():
    topology = Topology(n_atoms=1, n_groups=1, n_chains=1, n_molecules=1, n_entities=1)
    # `MolSys.__init__` builds an empty container from element counts; a topology is
    # assigned afterwards. Passing `topology=` used to be accepted and discarded, so this
    # read as if it carried the topology when it never did.
    molsys = MolSys()
    molsys.topology = topology

    assert digest_item(topology, form='molsysmt.Topology', caller='test') is topology
    assert digest_item(molsys, form='molsysmt.MolSys', caller='test') is molsys
    assert digest_item(None, caller='molsysmt.form.molsysmt_MolSys.append_structures') is None
    with pytest.raises(ArgumentError):
        digest_item(topology, form='molsysmt.MolSys', caller='test')
    with pytest.raises(ArgumentError):
        digest_item(object(), caller='test')


def test_digest_items_accepts_matching_form_sequences():
    topology = Topology(n_atoms=1, n_groups=1, n_chains=1, n_molecules=1, n_entities=1)
    # `MolSys.__init__` builds an empty container from element counts; a topology is
    # assigned afterwards. Passing `topology=` used to be accepted and discarded, so this
    # read as if it carried the topology when it never did.
    molsys = MolSys()
    molsys.topology = topology

    assert digest_items(molsys, caller='test') == [molsys]
    assert digest_items([topology, topology], forms='molsysmt.Topology', caller='test') == [topology, topology]
    with pytest.raises(ArgumentError):
        digest_items([topology, molsys], forms=['molsysmt.Topology', 'molsysmt.Topology'], caller='test')
    with pytest.raises(ArgumentError):
        digest_items(object(), caller='test')


def test_digest_keys_accepts_mutate_synonyms():
    assert digest_keys('group_index', caller='molsysmt.build.mutate.mutate') == 'group_index'
    assert digest_keys('residue_indices', caller='molsysmt.build.mutate.mutate') == 'group_index'
    assert digest_keys('group_id', caller='molsysmt.build.mutate.mutate') == 'group_id'
    assert digest_keys('residue_name', caller='molsysmt.build.mutate.mutate') == 'group_name'
    with pytest.raises(ArgumentError):
        digest_keys('bad', caller='molsysmt.build.mutate.mutate')
