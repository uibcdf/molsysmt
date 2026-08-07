import numpy as np
import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.atom_name import digest_atom_name
from molsysmt._private.argdigest.argument.atom_ff_type import digest_atom_ff_type
from molsysmt._private.argdigest.argument.atom_type import digest_atom_type
from molsysmt._private.argdigest.argument.group_name import digest_group_name
from molsysmt._private.argdigest.argument.group_type import digest_group_type
from molsysmt._private.argdigest.argument.component_name import digest_component_name
from molsysmt._private.argdigest.argument.component_type import digest_component_type
from molsysmt._private.argdigest.argument.chain_name import digest_chain_name
from molsysmt._private.argdigest.argument.chain_type import digest_chain_type
from molsysmt._private.argdigest.argument.molecule_name import digest_molecule_name
from molsysmt._private.argdigest.argument.molecule_type import digest_molecule_type
from molsysmt._private.argdigest.argument.entity_name import digest_entity_name
from molsysmt._private.argdigest.argument.entity_type import digest_entity_type


GET_CALLER = "molsysmt.basic.get.get"
COMPARE_CALLER = "molsysmt.basic.compare.compare"
FORM_CONVERTER_CALLER = "molsysmt.form.file_pdb.to_molsysmt_MolSys.to_molsysmt_MolSys"


def test_name_and_type_digesters_accept_builder_optional_none_values():
    assert digest_atom_name(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_atom") is None
    assert digest_atom_type(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_atom") is None
    assert digest_group_name(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_group") is None
    assert digest_group_type(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_group") is None
    assert digest_chain_name(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_chain") is None
    assert digest_chain_name(
        None,
        caller="molsysmt.native.molsys_builder.MolSysBuilder.assign_groups_to_new_chain",
    ) is None
    assert digest_chain_type(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_chain") is None
    assert digest_chain_type(
        None,
        caller="molsysmt.native.molsys_builder.MolSysBuilder.assign_groups_to_new_chain",
    ) is None
    assert digest_molecule_name(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_molecule") is None
    assert digest_molecule_type(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_molecule") is None
    assert digest_entity_name(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_entity") is None
    assert digest_entity_type(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_entity") is None


def test_atom_ff_type_supports_flags_and_label_collections():
    assert digest_atom_ff_type(True, caller=GET_CALLER) is True
    assert digest_atom_ff_type(('CT', 'HC')) == ['CT', 'HC']
    assert digest_atom_ff_type(np.array(['CT', 'HC'])) == ['CT', 'HC']


def test_name_and_type_digesters_support_boolean_and_form_converter_semantics():
    assert digest_atom_name(True, caller=GET_CALLER) is True
    assert digest_atom_type(False, caller=COMPARE_CALLER) is False
    assert digest_group_name(True, caller=GET_CALLER) is True
    assert digest_group_type(False, caller=GET_CALLER) is False
    assert digest_component_name(True, caller=GET_CALLER) is True
    assert digest_component_type(False, caller=GET_CALLER) is False
    assert digest_chain_name(True, caller=GET_CALLER) is True
    assert digest_chain_type(False, caller=COMPARE_CALLER) is False
    assert digest_molecule_name(True, caller=GET_CALLER) is True
    assert digest_molecule_type(False, caller=GET_CALLER) is False
    assert digest_entity_name(True, caller=GET_CALLER) is True
    assert digest_entity_type(False, caller=GET_CALLER) is False

    sentinel = object()
    assert digest_atom_name(sentinel, caller=FORM_CONVERTER_CALLER) is sentinel
    assert digest_group_type(sentinel, caller=FORM_CONVERTER_CALLER) is sentinel
    assert digest_component_name(sentinel, caller=FORM_CONVERTER_CALLER) is sentinel
    assert digest_component_type(sentinel, caller=FORM_CONVERTER_CALLER) is sentinel
    assert digest_chain_name(sentinel, caller=FORM_CONVERTER_CALLER) is sentinel
    assert digest_molecule_type(sentinel, caller=FORM_CONVERTER_CALLER) is sentinel
    assert digest_entity_name(sentinel, caller=FORM_CONVERTER_CALLER) is sentinel


@pytest.mark.parametrize(
    "digester, value",
    [
        (digest_atom_name, "CA"),
        (digest_atom_type, "C"),
        (digest_group_name, "ALA"),
        (digest_group_type, "amino acid"),
        (digest_component_name, "protein 0"),
        (digest_component_type, "protein"),
        (digest_chain_name, "A"),
        (digest_chain_type, "protein"),
        (digest_molecule_name, "LIG"),
        (digest_molecule_type, "small molecule"),
        (digest_entity_name, "lysozyme"),
        (digest_entity_type, "protein"),
    ],
)
def test_name_and_type_digesters_normalize_scalar_and_sequence_inputs(digester, value):
    assert digester(value) == value
    assert digester([value]) == [value]
    assert digester((value,)) == [value]
    assert digester(np.array([value], dtype=object)) == [value]


@pytest.mark.parametrize(
    "digester",
    [
        digest_atom_name,
        digest_atom_type,
        digest_group_name,
        digest_group_type,
        digest_component_name,
        digest_component_type,
        digest_chain_name,
        digest_chain_type,
        digest_molecule_name,
        digest_molecule_type,
        digest_entity_name,
        digest_entity_type,
    ],
)
def test_name_and_type_digesters_reject_invalid_inputs(digester):
    with pytest.raises(ArgumentError):
        digester({"invalid": "value"})
