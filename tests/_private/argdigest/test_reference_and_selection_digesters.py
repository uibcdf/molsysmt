import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest.argument.reference_coordinates import digest_reference_coordinates
from molsysmt._private.argdigest.argument.reference_molecular_system import digest_reference_molecular_system
from molsysmt._private.argdigest.argument.reference_selection import digest_reference_selection
from molsysmt._private.argdigest.argument.reference_selection_fit import digest_reference_selection_fit
from molsysmt._private.argdigest.argument.reference_structure_index import digest_reference_structure_index
from molsysmt._private.argdigest.argument.reference_structure_indices import digest_reference_structure_indices
from molsysmt._private.argdigest.argument.reference_weights import digest_reference_weights
from molsysmt._private.argdigest.argument.selection_A import digest_selection_A
from molsysmt._private.argdigest.argument.selection_B import digest_selection_B
from molsysmt._private.argdigest.argument.structure_indices_A import digest_structure_indices_A
from molsysmt._private.argdigest.argument.structure_indices_B import digest_structure_indices_B
from molsysmt._private.smonitor import ArgumentError


def test_reference_and_selection_digesters(builder_pdb_molsys):
    coords = puw.quantity(np.zeros((1, 4, 3), dtype=float), 'nm')
    assert digest_reference_coordinates(coords).shape == (1, 4, 3)
    assert digest_reference_molecular_system(builder_pdb_molsys) is builder_pdb_molsys
    assert digest_reference_selection('atom_index<3') == 'atom_index<3'
    assert digest_reference_selection_fit('atom_index<3') == 'atom_index<3'
    assert digest_reference_structure_index(0) == 0
    assert digest_reference_structure_indices([0, 1]) == [0, 1]
    assert np.array_equal(digest_reference_weights([1.0, 2.0]), np.array([1.0, 2.0]))
    assert digest_selection_A('atom_index==0') == 'atom_index==0'
    assert digest_selection_B('atom_index==1') == 'atom_index==1'
    assert digest_structure_indices_A([0]) == [0]
    assert np.array_equal(digest_structure_indices_B([0, 1]), np.array([0, 1], dtype='int64'))

    with pytest.raises(ArgumentError):
        digest_reference_structure_index('0')
    with pytest.raises(ArgumentError):
        digest_reference_molecular_system(object())
