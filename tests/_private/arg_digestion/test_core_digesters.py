import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.atom_id import digest_atom_id
from molsysmt._private.argdigest.argument.atom_index import digest_atom_index
from molsysmt._private.argdigest.argument.atom_indices import digest_atom_indices
from molsysmt._private.argdigest.argument.atom_name import digest_atom_name
from molsysmt._private.argdigest.argument.atom_names import digest_atom_names
from molsysmt._private.argdigest.argument.atom_type import digest_atom_type
from molsysmt._private.argdigest.argument.chain_id import digest_chain_id
from molsysmt._private.argdigest.argument.chain_index import digest_chain_index
from molsysmt._private.argdigest.argument.chain_name import digest_chain_name
from molsysmt._private.argdigest.argument.chain_type import digest_chain_type
from molsysmt._private.argdigest.argument.component_id import digest_component_id
from molsysmt._private.argdigest.argument.component_index import digest_component_index
from molsysmt._private.argdigest.argument.component_name import digest_component_name
from molsysmt._private.argdigest.argument.component_type import digest_component_type
from molsysmt._private.argdigest.argument.coordinates import digest_coordinates
from molsysmt._private.argdigest.argument.box import digest_box
from molsysmt._private.argdigest.argument.box_angles import digest_box_angles
from molsysmt._private.argdigest.argument.box_center import digest_box_center
from molsysmt._private.argdigest.argument.box_lengths import digest_box_lengths
from molsysmt._private.argdigest.argument.box_origin import digest_box_origin
from molsysmt._private.argdigest.argument.b_factor import digest_b_factor
from molsysmt._private.argdigest.argument.engine import digest_engine
from molsysmt._private.argdigest.argument.entity_id import digest_entity_id
from molsysmt._private.argdigest.argument.entity_index import digest_entity_index
from molsysmt._private.argdigest.argument.entity_name import digest_entity_name
from molsysmt._private.argdigest.argument.entity_type import digest_entity_type
from molsysmt._private.argdigest.argument.form import digest_form
from molsysmt._private.argdigest.argument.group_id import digest_group_id
from molsysmt._private.argdigest.argument.group_name import digest_group_name
from molsysmt._private.argdigest.argument.group_type import digest_group_type
from molsysmt._private.argdigest.argument.molecule_id import digest_molecule_id
from molsysmt._private.argdigest.argument.molecule_name import digest_molecule_name
from molsysmt._private.argdigest.argument.molecule_type import digest_molecule_type
from molsysmt._private.argdigest.argument.n_atoms import digest_n_atoms
from molsysmt._private.argdigest.argument.n_chains import digest_n_chains
from molsysmt._private.argdigest.argument.n_components import digest_n_components
from molsysmt._private.argdigest.argument.n_entities import digest_n_entities
from molsysmt._private.argdigest.argument.n_molecules import digest_n_molecules
from molsysmt._private.argdigest.argument.show import digest_show
from molsysmt._private.argdigest.argument.style import digest_style


BOOL_CALLER = "molsysmt.basic.get.get"
FORM_CONVERTER_CALLER = "molsysmt.form.file_pdb.to_molsysmt_MolSys.to_molsysmt_MolSys"
CHAIN_BUILDER_CALLER = "molsysmt.native.molsys_builder.MolSysBuilder.add_chain"
SHOW_CONTACTS_CALLER = "molsysmt.structure.show_contacts.show_contacts"


@pytest.mark.parametrize(
    ("digester", "scalar", "tuple_value", "array_value"),
    [
        (digest_atom_id, 5, (5, 6), np.array([5, 6])),
        (digest_atom_index, 5, (5, 6), np.array([5, 6])),
        (digest_component_id, 2, (2, 3), np.array([2, 3])),
        (digest_component_index, 2, (2, 3), np.array([2, 3])),
        (digest_entity_id, 1, (1, 2), np.array([1, 2])),
        (digest_entity_index, 1, (1, 2), np.array([1, 2])),
        (digest_group_id, 7, (7, 8), np.array([7, 8])),
        (digest_molecule_id, 9, (9, 10), np.array([9, 10])),
        (digest_chain_id, 3, (3, 4), np.array([3, 4])),
        (digest_chain_index, 3, (3, 4), np.array([3, 4])),
    ],
)
def test_index_like_digesters_normalize_iterables(digester, scalar, tuple_value, array_value):
    assert digester(scalar) == [scalar]
    assert digester(list(tuple_value)) == list(tuple_value)
    assert digester(tuple_value) == list(tuple_value)
    assert digester(array_value) == list(array_value)


@pytest.mark.parametrize(
    ("digester", "valid_value"),
    [
        (digest_atom_id, True),
        (digest_atom_index, True),
        (digest_atom_name, True),
        (digest_atom_type, True),
        (digest_component_id, True),
        (digest_component_index, True),
        (digest_component_name, True),
        (digest_component_type, True),
        (digest_entity_id, True),
        (digest_entity_index, True),
        (digest_entity_name, True),
        (digest_entity_type, True),
        (digest_group_id, True),
        (digest_group_name, True),
        (digest_group_type, True),
        (digest_molecule_id, True),
        (digest_molecule_name, True),
        (digest_molecule_type, True),
        (digest_chain_id, True),
        (digest_chain_index, True),
        (digest_chain_name, True),
        (digest_chain_type, True),
    ],
)
def test_boolean_query_digesters_accept_bool_only_when_caller_requests_it(digester, valid_value):
    assert digester(valid_value, caller=BOOL_CALLER) is True


@pytest.mark.parametrize(
    ("digester", "bad_value"),
    [
        (digest_atom_index, "CA"),
        (digest_component_index, "0"),
        (digest_entity_index, "1"),
        (digest_chain_index, "2"),
    ],
)
def test_boolean_query_index_digesters_reject_non_boolean_values(digester, bad_value):
    with pytest.raises(ArgumentError):
        digester(bad_value, caller=BOOL_CALLER)


@pytest.mark.parametrize(
    ("digester", "value"),
    [
        (digest_atom_name, "CA"),
        (digest_atom_type, "protein"),
        (digest_component_name, "peptide 0"),
        (digest_component_type, "peptide"),
        (digest_entity_name, "protein 0"),
        (digest_entity_type, "protein"),
        (digest_group_id, ["0", "1"]),
        (digest_group_name, ["ALA", "GLY"]),
        (digest_group_type, ["amino acid", "amino acid"]),
        (digest_molecule_id, ["0", "1"]),
        (digest_molecule_name, ["protein 0", "water"]),
        (digest_molecule_type, ["protein", "water"]),
        (digest_chain_name, "A"),
        (digest_chain_type, "protein"),
        (digest_component_id, ["0", "1"]),
        (digest_entity_id, ["0", "1"]),
    ],
)
def test_form_converter_bypass_digesters_return_raw_value(digester, value):
    assert digester(value, caller=FORM_CONVERTER_CALLER) == value


def test_add_chain_digesters_accept_native_builder_values():
    assert digest_chain_id(4, caller=CHAIN_BUILDER_CALLER) == 4
    assert digest_chain_id(None, caller=CHAIN_BUILDER_CALLER) is None
    assert digest_chain_name("B", caller=CHAIN_BUILDER_CALLER) == "B"
    assert digest_chain_name(None, caller=CHAIN_BUILDER_CALLER) is None


def test_chain_id_normalizes_scalar_string_for_public_set():
    assert digest_chain_id("PROTEIN", caller="molsysmt.basic.set.set") == ["PROTEIN"]


def test_atom_indices_handles_all_scalar_arrays_and_nested_values():
    assert digest_atom_indices(None) is None
    assert digest_atom_indices("all") == "all"
    np.testing.assert_array_equal(digest_atom_indices(3), np.array([3], dtype=np.int64))
    np.testing.assert_array_equal(digest_atom_indices([1, 2]), np.array([1, 2], dtype=np.int64))
    nested = digest_atom_indices([[1, 2], [3]])
    assert len(nested) == 2
    np.testing.assert_array_equal(nested[0], np.array([1, 2], dtype=np.int64))
    np.testing.assert_array_equal(nested[1], np.array([3], dtype=np.int64))


def test_atom_names_normalize_supported_inputs():
    assert digest_atom_names(None) is None
    assert digest_atom_names("all") == "all"
    assert digest_atom_names("CA") == ["CA"]
    assert digest_atom_names(("CA", "CB")) == ["CA", "CB"]
    assert digest_atom_names(np.array(["CA", "CB"], dtype=object)) == ["CA", "CB"]


@pytest.mark.parametrize(
    ("digester", "value", "expected"),
    [
        (digest_group_name, "ALA", "ALA"),
        (digest_group_name, ("ALA", "GLY"), ["ALA", "GLY"]),
        (digest_group_name, np.array(["ALA", "GLY"], dtype=object), ["ALA", "GLY"]),
        (digest_molecule_name, "protein 0", "protein 0"),
        (digest_molecule_name, ("protein 0", "water"), ["protein 0", "water"]),
        (digest_molecule_type, "protein", "protein"),
        (digest_molecule_type, ("protein", "water"), ["protein", "water"]),
        (digest_entity_name, ("protein 0", "water"), ["protein 0", "water"]),
        (digest_entity_type, ("protein", "water"), ["protein", "water"]),
    ],
)
def test_name_and_type_digesters_normalize_without_form_caller(digester, value, expected):
    assert digester(value) == expected


@pytest.mark.parametrize(
    ("digester", "caller", "good_value"),
    [
        (digest_n_atoms, "molsysmt.native.topology.__init__", 10),
        (digest_n_atoms, "molsysmt.basic.contains.contains", 10),
        (digest_n_components, "molsysmt.native.topology.__init__", 3),
        (digest_n_entities, "molsysmt.native.molsys.__init__", 2),
        (digest_n_molecules, "molsysmt.basic.is_composed_of.is_composed_of", 4),
        (digest_n_chains, "molsysmt.basic.contains.contains", 1),
    ],
)
def test_n_digesters_accept_native_and_composition_contexts(digester, caller, good_value):
    assert digester(good_value, caller=caller) == good_value


@pytest.mark.parametrize(
    "digester",
    [
        digest_n_atoms,
        digest_n_components,
        digest_n_entities,
        digest_n_molecules,
        digest_n_chains,
    ],
)
def test_n_digesters_accept_boolean_query_contract(digester):
    assert digester(True, caller=BOOL_CALLER) is True


def test_form_digester_normalizes_case_and_accepts_lists_and_files():
    assert digest_form("MOLSYSMT.MOLSYS") == "molsysmt.MolSys"
    assert digest_form(["molsysmt.molsys", "STRING:PDB_ID"]) == ["molsysmt.MolSys", "string:pdb_id"]
    assert digest_form("trajectory.xtc") == "trajectory.xtc"
    assert digest_form(True, caller="molsysmt.basic.compare.compare") is True
    with pytest.raises(ArgumentError):
        digest_form("definitely:not_a_form")


def test_engine_show_and_style_digesters_validate_expected_contracts():
    assert digest_engine("molsysmt") == "MolSysMT"
    with pytest.raises(ArgumentError):
        digest_engine("unknown-engine")

    assert digest_show(True) is True
    with pytest.raises(ArgumentError):
        digest_show("yes")

    assert digest_style("plotly", caller=SHOW_CONTACTS_CALLER) == "plotly"
    assert digest_style("matplotlib", caller=SHOW_CONTACTS_CALLER) == "matplotlib"
    with pytest.raises(ArgumentError):
        digest_style("text", caller=SHOW_CONTACTS_CALLER)


def test_coordinates_digester_normalizes_rank_and_dtype():
    one_atom = puw.quantity([1.0, 2.0, 3.0], "angstroms")
    out = digest_coordinates(one_atom)
    assert puw.get_value(out).shape == (1, 1, 3)
    assert puw.get_value(out).dtype == np.float64

    many_atoms = puw.quantity([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "angstroms")
    out = digest_coordinates(many_atoms)
    assert puw.get_value(out).shape == (1, 2, 3)

    trajectory = puw.quantity(np.ones((2, 3, 3), dtype=np.float32), "nanometers")
    out = digest_coordinates(trajectory)
    assert puw.get_value(out).shape == (2, 3, 3)
    assert puw.get_value(out).dtype == np.float64
    assert digest_coordinates(True, caller=BOOL_CALLER) is True


def test_box_digesters_normalize_shapes_and_units():
    box = puw.quantity(np.eye(3), "nanometers")
    out = digest_box(box)
    assert puw.get_value(out).shape == (1, 3, 3)

    lengths = digest_box_lengths(puw.quantity([1.0, 2.0, 3.0], "nanometers"))
    assert puw.get_value(lengths).shape == (1, 3)

    angles = digest_box_angles(puw.quantity([90.0, 90.0, 120.0], "degrees"))
    assert puw.get_value(angles).shape == (1, 3)

    origin = digest_box_origin(puw.quantity([[0.0, 0.0, 0.0]], "nanometers"))
    assert puw.get_value(origin).shape == (3,)

    center = digest_box_center(puw.quantity([[[0.0, 0.0, 0.0]]], "nanometers"))
    assert puw.get_value(center).shape == (3,)

    assert digest_box(True, caller=BOOL_CALLER) is True
    assert digest_box_lengths(True, caller=BOOL_CALLER) is True
    assert digest_box_angles(True, caller=BOOL_CALLER) is True


def test_b_factor_digester_normalizes_rank_and_preserves_boolean_query_mode():
    values = puw.quantity(np.arange(3.0), "angstroms**2")
    out = digest_b_factor(values)
    assert puw.get_value(out).shape == (1, 3)

    matrix = puw.quantity(np.ones((2, 3), dtype=np.float32), "angstroms**2")
    out = digest_b_factor(matrix)
    assert puw.get_value(out).shape == (2, 3)

    assert digest_b_factor(True, caller=BOOL_CALLER) is True

    with pytest.raises(ArgumentError):
        digest_b_factor(puw.quantity([1.0, 2.0], "nanometers"))
