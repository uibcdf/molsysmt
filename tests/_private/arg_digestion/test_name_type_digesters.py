import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.atom_name import digest_atom_name
from molsysmt._private.arg_digestion.argument.atom_type import digest_atom_type
from molsysmt._private.arg_digestion.argument.group_name import digest_group_name
from molsysmt._private.arg_digestion.argument.group_type import digest_group_type
from molsysmt._private.arg_digestion.argument.component_name import digest_component_name
from molsysmt._private.arg_digestion.argument.component_type import digest_component_type
from molsysmt._private.arg_digestion.argument.molecule_name import digest_molecule_name
from molsysmt._private.arg_digestion.argument.molecule_type import digest_molecule_type
from molsysmt._private.arg_digestion.argument.entity_name import digest_entity_name
from molsysmt._private.arg_digestion.argument.entity_type import digest_entity_type
from molsysmt._private.arg_digestion.argument.chain_name import digest_chain_name
from molsysmt._private.arg_digestion.argument.chain_type import digest_chain_type


@pytest.mark.parametrize(
    ("digester", "value"),
    [
        (digest_atom_name, True),
        (digest_atom_type, True),
        (digest_group_name, True),
        (digest_group_type, True),
        (digest_component_name, True),
        (digest_component_type, True),
        (digest_molecule_name, True),
        (digest_molecule_type, True),
        (digest_entity_name, True),
        (digest_entity_type, True),
        (digest_chain_name, True),
        (digest_chain_type, True),
    ],
)
def test_name_and_type_digesters_accept_boolean_for_get(digester, value):
    assert digester(value, caller='molsysmt.basic.get.get') is True


@pytest.mark.parametrize(
    ("digester", "value"),
    [
        (digest_atom_name, 'CA'),
        (digest_atom_type, 'C'),
        (digest_group_name, 'ALA'),
        (digest_group_type, 'amino acid'),
        (digest_component_name, 'protein 0'),
        (digest_component_type, 'protein'),
        (digest_molecule_name, 'water'),
        (digest_molecule_type, 'water'),
        (digest_entity_name, 'protein 0'),
        (digest_entity_type, 'protein'),
        (digest_chain_name, 'A'),
        (digest_chain_type, 'protein'),
    ],
)
def test_name_and_type_digesters_accept_string_values(digester, value):
    assert digester(value, caller=None) == value


@pytest.mark.parametrize(
    ("digester", "values", "expected"),
    [
        (digest_atom_name, ['CA', 'CB'], ['CA', 'CB']),
        (digest_atom_type, ['C', 'O'], ['C', 'O']),
        (digest_group_name, ['ALA', 'GLY'], ['ALA', 'GLY']),
        (digest_group_type, ['protein', 'water'], ['protein', 'water']),
        (digest_component_name, ['protein 0', 'water'], ['protein 0', 'water']),
        (digest_component_type, ['protein', 'water'], ['protein', 'water']),
        (digest_molecule_name, ['protein 0', 'water'], ['protein 0', 'water']),
        (digest_molecule_type, ['protein', 'water'], ['protein', 'water']),
        (digest_entity_name, ['protein 0', 'water'], ['protein 0', 'water']),
        (digest_entity_type, ['protein', 'water'], ['protein', 'water']),
        (digest_chain_name, ['A', 'B'], ['A', 'B']),
        (digest_chain_type, ['protein', 'water'], ['protein', 'water']),
    ],
)
def test_name_and_type_digesters_accept_iterables(digester, values, expected):
    assert digester(values, caller=None) == expected


@pytest.mark.parametrize(
    ("digester", "value"),
    [
        (digest_atom_name, 3.14),
        (digest_atom_type, 3.14),
        (digest_group_name, {'ALA'}),
        (digest_group_type, {'protein'}),
        (digest_component_name, 3.14),
        (digest_component_type, {'protein'}),
        (digest_molecule_name, 3.14),
        (digest_molecule_type, {'protein'}),
        (digest_entity_name, 3.14),
        (digest_entity_type, {'protein'}),
        (digest_chain_name, 3.14),
        (digest_chain_type, {'protein'}),
    ],
)
def test_name_and_type_digesters_reject_invalid_values(digester, value):
    with pytest.raises(ArgumentError):
        digester(value, caller='molsysmt.basic.convert.convert')
