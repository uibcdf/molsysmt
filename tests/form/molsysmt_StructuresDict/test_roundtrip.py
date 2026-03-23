"""
Contract and parity tests for molsysmt.StructuresDict form.

Oracle: builder_pdb_molsys (4 atoms, 1 frame).
Parity means that Structures → StructuresDict → Structures round-trip
preserves n_atoms, n_structures, and all coordinate values.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture()
def source_structures(builder_pdb_molsys):
    return builder_pdb_molsys.structures


@pytest.fixture()
def structures_dict(source_structures):
    return msm.convert(source_structures, to_form='molsysmt.StructuresDict')


@pytest.fixture()
def rebuilt_structures(structures_dict):
    return msm.convert(structures_dict, to_form='molsysmt.Structures')


# ---------------------------------------------------------------------------
# Contract: molsysmt.StructuresDict can be created and queried
# ---------------------------------------------------------------------------

def test_structures_dict_is_dict(structures_dict):
    assert isinstance(structures_dict, dict)


def test_structures_dict_n_atoms(structures_dict):
    assert msm.get(structures_dict, element='system', n_atoms=True) == 4


def test_structures_dict_n_structures(structures_dict):
    assert msm.get(structures_dict, element='system', n_structures=True) == 1


# ---------------------------------------------------------------------------
# Parity: Structures → StructuresDict → Structures preserves data
# ---------------------------------------------------------------------------

def test_parity_atom_count(rebuilt_structures, source_structures):
    assert rebuilt_structures.n_atoms == source_structures.n_atoms


def test_parity_structure_count(rebuilt_structures, source_structures):
    assert rebuilt_structures.n_structures == source_structures.n_structures


def test_parity_coordinates(rebuilt_structures, source_structures):
    rebuilt_coords = puw.get_value(rebuilt_structures.coordinates, to_unit='nm')
    source_coords = puw.get_value(source_structures.coordinates, to_unit='nm')
    assert np.allclose(rebuilt_coords, source_coords)


def test_roundtrip_preserves_builder_truth(builder_structures, tmp_path):
    structures_dict = msm.convert(builder_structures, to_form='molsysmt.StructuresDict')
    rebuilt = msm.convert(structures_dict, to_form='molsysmt.Structures')

    assert rebuilt.n_atoms == 4
    assert rebuilt.n_structures == 1
    rebuilt_coords = puw.get_value(rebuilt.coordinates, to_unit='nm')
    source_coords = puw.get_value(builder_structures.coordinates, to_unit='nm')
    assert np.allclose(rebuilt_coords, source_coords)
