import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.angles import digest_angles
from molsysmt._private.arg_digestion.argument.atom_pair import digest_atom_pair
from molsysmt._private.arg_digestion.argument.atom_pairs import digest_atom_pairs
from molsysmt._private.arg_digestion.argument.bond_id import digest_bond_id
from molsysmt._private.arg_digestion.argument.bond_index import digest_bond_index
from molsysmt._private.arg_digestion.argument.bond_indices import digest_bond_indices
from molsysmt._private.arg_digestion.argument.bond_length import digest_bond_length
from molsysmt._private.arg_digestion.argument.bond_order import digest_bond_order
from molsysmt._private.arg_digestion.argument.bond_type import digest_bond_type
from molsysmt._private.arg_digestion.argument.bonded_atom_pairs import digest_bonded_atom_pairs
from molsysmt._private.arg_digestion.argument.bonded_atoms import digest_bonded_atoms
from molsysmt._private.arg_digestion.argument.dihedral_angle import digest_dihedral_angle
from molsysmt._private.arg_digestion.argument.distance import digest_distance

GET_CALLER = "molsysmt.basic.get.get"
COMPARE_CALLER = "molsysmt.basic.compare.compare"
SELECT_CALLER = "molsysmt.basic.select.select"
HBOND_CALLER = "molsysmt.molecular_mechanics.add_harmonic_bond_force.add_harmonic_bond_force"
CONTACTS_CALLER = "molsysmt.third_party.nglview.add_contacts.add_contacts"
LEGACY_ADD_BONDS_CALLER = "molsysmt.build.add_bonds.add_bonds"
DIHEDRAL_CALLER = "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"


def test_angles_and_distance_digesters_normalize_quantities():
    angles = digest_angles("90 degrees")
    assert angles.shape == (1, 1)

    vector = digest_angles(msm.pyunitwizard.quantity([90.0, 120.0], "degrees"))
    assert vector.shape == (1, 2)

    matrix = digest_angles(msm.pyunitwizard.quantity([[90.0, 120.0], [60.0, 180.0]], "degrees"))
    assert matrix.shape == (2, 2)

    distance = digest_distance("0.25 nm")
    assert msm.pyunitwizard.get_value(distance) == pytest.approx(0.25)

    with pytest.raises(ArgumentError):
        digest_distance(msm.pyunitwizard.quantity(1.0, "degrees"))


def test_atom_pair_and_atom_pairs_digesters_support_supported_callers():
    assert digest_atom_pair([1, 2], caller=HBOND_CALLER) == [[1, 2]]
    assert digest_atom_pair(np.array([1, 2]), caller=HBOND_CALLER) == [[np.int64(1), np.int64(2)]]
    assert digest_atom_pair([(1, 2), (3, 4)], caller=HBOND_CALLER) == [[1, 2], [3, 4]]

    assert digest_atom_pairs([1, 2], caller=HBOND_CALLER) == [[1, 2]]
    assert np.array_equal(digest_atom_pairs([1, 2], caller=CONTACTS_CALLER), np.array([[1, 2]]))
    assert np.array_equal(
        digest_atom_pairs([(1, 2), (3, 4)], caller=CONTACTS_CALLER),
        np.array([[1, 2], [3, 4]]),
    )
    assert digest_atom_pairs(None, caller=CONTACTS_CALLER) is None

    with pytest.raises(ArgumentError):
        digest_atom_pair([1, 2], caller=GET_CALLER)


def test_bond_id_index_and_type_digesters_cover_public_callers():
    assert digest_bond_id(True, caller=GET_CALLER) is True
    assert digest_bond_id(True, caller=COMPARE_CALLER) is True
    assert digest_bond_id("all", caller=SELECT_CALLER) == "all"
    assert digest_bond_id(["1", "2"], caller=SELECT_CALLER) == ["1", "2"]

    assert digest_bond_index(True, caller=GET_CALLER) is True
    assert digest_bond_index(True, caller=COMPARE_CALLER) is True
    assert digest_bond_index("all", caller=SELECT_CALLER) == "all"
    assert digest_bond_index([1, 2], caller=SELECT_CALLER) == [1, 2]

    assert digest_bond_type(True, caller=GET_CALLER) is True
    assert digest_bond_type(True, caller=COMPARE_CALLER) is True
    assert digest_bond_type("all", caller=SELECT_CALLER) == "all"
    assert digest_bond_type(["single", "double"], caller=SELECT_CALLER) == ["single", "double"]
    assert digest_bond_type(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_bond") is None


def test_bond_indices_and_bonded_atom_digesters_cover_valid_inputs():
    assert np.array_equal(digest_bond_indices(3), np.array([3], dtype="int64"))
    assert np.array_equal(digest_bond_indices([1, 2]), np.array([1, 2], dtype="int64"))
    assert digest_bond_indices("all") == "all"
    assert digest_bond_indices(None) is None

    nested = digest_bond_indices([[1, 2], [3, 4]])
    assert all(isinstance(item, np.ndarray) for item in nested)

    assert digest_bonded_atoms(True, caller=GET_CALLER) is True
    assert np.array_equal(
        digest_bonded_atom_pairs([[1, 2], [3, 4]], caller=LEGACY_ADD_BONDS_CALLER),
        np.array([[1, 2], [3, 4]]),
    )

    with pytest.raises(ArgumentError):
        digest_bonded_atom_pairs([[1, 2, 3]], caller=LEGACY_ADD_BONDS_CALLER)


def test_bond_length_order_type_and_dihedral_angle_digesters_cover_supported_cases():
    single = digest_bond_length("0.12 nm", caller=HBOND_CALLER)
    assert msm.pyunitwizard.get_value(single) == pytest.approx(0.12)

    many = digest_bond_length(
        [
            msm.pyunitwizard.quantity(0.12, "nanometers"),
            msm.pyunitwizard.quantity(0.14, "nanometers"),
        ],
        caller=HBOND_CALLER,
    )
    assert len(many) == 2

    assert digest_bond_order(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_bond") is None
    assert digest_bond_type(None, caller="molsysmt.native.molsys_builder.MolSysBuilder.add_bond") is None

    assert digest_dihedral_angle("phi", caller=DIHEDRAL_CALLER) == "phi"
    assert digest_dihedral_angle("all") == "all"
    assert digest_dihedral_angle(None) is None

    with pytest.raises(ArgumentError):
        digest_dihedral_angle("unknown", caller=DIHEDRAL_CALLER)
