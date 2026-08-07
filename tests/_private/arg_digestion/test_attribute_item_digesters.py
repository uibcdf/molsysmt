import pytest

from molsysmt import MolSysBuilder
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.attribute import digest_attribute
from molsysmt._private.argdigest.argument.attribute_type import digest_attribute_type
from molsysmt._private.argdigest.argument.keys import digest_keys
from molsysmt._private.argdigest.argument.items import digest_items
from molsysmt._private.argdigest.argument.value import digest_value


def test_attribute_and_attribute_type_digesters_accept_supported_values():
    assert digest_attribute('atom_name') == 'atom_name'
    assert digest_attribute('Topological', caller='molsysmt.basic.has_attribute.has_attribute') == 'topological'
    with pytest.raises(ArgumentError):
        digest_attribute('not_an_attribute')

    caller = 'molsysmt.basic.compare.compare'
    assert digest_attribute_type(None, caller=caller) is None
    assert digest_attribute_type('all', caller=caller) == 'all'
    assert digest_attribute_type('Structural', caller=caller) == 'structural'
    with pytest.raises(ArgumentError):
        digest_attribute_type('foo', caller=caller)


def test_keys_and_items_digesters_resolve_supported_inputs():
    mutate_caller = 'molsysmt.build.mutate.mutate'
    assert digest_keys('residue_names', caller=mutate_caller) == 'group_name'
    assert digest_keys('group_id', caller=mutate_caller) == 'group_id'
    with pytest.raises(ArgumentError):
        digest_keys('atom_name', caller=mutate_caller)

    builder = MolSysBuilder()
    builder.add_atom(atom_name='Ar', atom_type='Ar')
    molsys = builder.build()
    accepted = digest_items([molsys], forms='molsysmt.MolSys')
    assert accepted == [molsys]
    with pytest.raises(ArgumentError):
        digest_items([molsys], forms='molsysmt.Topology')
    with pytest.raises(ArgumentError):
        digest_items([object()])


def test_value_digesters_dispatch_to_expected_setter_digesters():
    assert digest_value('CA', caller='molsysmt.form.molsysmt_MolSys.set_atom_name_to_atom') == 'CA'
    assert digest_value('12', caller='molsysmt.form.molsysmt_MolSys.set_group_id_to_atom') == '12'
    assert digest_value('protein', caller='molsysmt.form.molsysmt_MolSys.set_chain_type_to_group') == 'protein'
    with pytest.raises(ArgumentError):
        digest_value('bad', caller='molsysmt.form.molsysmt_MolSys.set_structure_id_to_system')
