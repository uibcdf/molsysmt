import numpy as np
import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.atom_pair import digest_atom_pair
from molsysmt._private.argdigest.argument.atom_pairs import digest_atom_pairs
from molsysmt._private.argdigest.argument.bond_length import digest_bond_length
from molsysmt._private.argdigest.argument.chain_indices import digest_chain_indices
from molsysmt._private.argdigest.argument.dihedral_quartets import digest_dihedral_quartets
from molsysmt._private.argdigest.argument.direction import digest_direction
from molsysmt._private.argdigest.argument.force_constant import digest_force_constant
from molsysmt._private.argdigest.argument.location_id import digest_location_id
from molsysmt._private.argdigest.argument.output_indices import digest_output_indices
from molsysmt._private.argdigest.argument.output_structure_indices import digest_output_structure_indices
from molsysmt._private.argdigest.argument.output_type import digest_output_type
from molsysmt._private.argdigest.argument.shape import digest_shape
from molsysmt import pyunitwizard as puw


HBOND_CALLER = "molsysmt.molecular_mechanics.add_harmonic_bond_force.add_harmonic_bond_force"
ADD_CONTACTS_CALLER = "molsysmt.third_party.nglview.add_contacts.add_contacts"
CONTACTS_CALLER = "molsysmt.structure.get_contacts.get_contacts"
DISTANCES_CALLER = "molsysmt.structure.get_distances.get_distances"
NEIGHBORS_CALLER = "molsysmt.structure.get_neighbors.get_neighbors"
MOVE_AWAY_CALLER = "molsysmt.structure.move_away.move_away"
ALTLOC_CALLER = "molsysmt.build.solve_atoms_with_alternate_location.solve_atoms_with_alternate_location"


def test_atom_pair_and_atom_pairs_digesters_normalize_force_and_contact_inputs():
    assert digest_atom_pair((1, 2), caller=HBOND_CALLER) == [[1, 2]]
    assert digest_atom_pair(np.array([1, 2]), caller=HBOND_CALLER) == [[1, 2]]

    assert digest_atom_pairs((1, 2), caller=HBOND_CALLER) == [[1, 2]]
    assert digest_atom_pairs([(1, 2), (3, 4)], caller=HBOND_CALLER) == [[1, 2], [3, 4]]

    out = digest_atom_pairs([(1, 2), (3, 4)], caller=ADD_CONTACTS_CALLER)
    np.testing.assert_array_equal(out, np.array([[1, 2], [3, 4]]))
    assert digest_atom_pairs(None, caller=ADD_CONTACTS_CALLER) is None


def test_bond_length_and_force_constant_digesters_normalize_scalar_and_iterable_quantities():
    length = digest_bond_length(puw.quantity(0.12, "nanometers"), caller=HBOND_CALLER)
    assert puw.is_quantity(length)

    lengths = digest_bond_length(puw.quantity([0.12, 0.13], "nanometers"), caller=HBOND_CALLER)
    assert len(lengths) == 2

    constant = digest_force_constant(puw.quantity(300.0, "kilojoule/(nanometer**2*mole)"), caller=HBOND_CALLER)
    assert len(constant) == 1

    constants = digest_force_constant(
        puw.quantity([300.0, 400.0], "kilojoule/(nanometer**2*mole)"),
        caller=HBOND_CALLER,
    )
    assert len(constants) == 2


def test_chain_indices_and_location_id_digesters_cover_special_cases():
    np.testing.assert_array_equal(digest_chain_indices(3), np.array([3], dtype=np.int64))
    assert digest_chain_indices("all") == "all"

    nested = digest_chain_indices([np.array([0, 1]), np.array([2])], caller="digest_bioassembly")
    assert len(nested) == 2

    assert digest_location_id("occupancy", caller=ALTLOC_CALLER) == "occupancy"
    np.testing.assert_array_equal(digest_location_id(["A", "B"]), np.array(["A", "B"]))


def test_output_helpers_and_shape_digesters_validate_caller_specific_contracts():
    assert digest_output_indices("selection", caller=CONTACTS_CALLER) == "selection"
    assert digest_output_indices("atom", caller=DISTANCES_CALLER) == "atom"
    assert digest_output_structure_indices("structure", caller=NEIGHBORS_CALLER) == "structure"

    assert digest_output_type("dictionary", caller="molsysmt.basic.get.get") == "dictionary"
    assert digest_output_type("pairs", caller=CONTACTS_CALLER) == "pairs"
    assert digest_output_type("numpy.ndarray", caller=DISTANCES_CALLER) == "numpy.ndarray"

    assert digest_shape("cubic", caller="molsysmt.structure.get_box_with_shape") == "cubic"


def test_direction_digester_normalizes_vectors_and_allows_none_for_move_away():
    assert digest_direction(None, caller=MOVE_AWAY_CALLER) is None

    out = digest_direction([1.0, 0.0, 0.0])
    assert out.shape == (1, 3)
    np.testing.assert_allclose(out[0], np.array([1.0, 0.0, 0.0]))

    out = digest_direction(np.array([[1.0, 0.0, 0.0], [0.0, 3.0, 0.0]]))
    np.testing.assert_allclose(out, np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]))


def test_dihedral_quartets_and_invalid_caller_paths_raise_argument_error():
    out = digest_dihedral_quartets([[0, 1, 2, 3], [1, 2, 3, 4]])
    assert out.shape == (2, 4)

    with pytest.raises(ArgumentError):
        digest_atom_pairs([(1, 2)], caller=None)

    with pytest.raises(ArgumentError):
        digest_output_type("bad", caller="molsysmt.basic.get.get")
