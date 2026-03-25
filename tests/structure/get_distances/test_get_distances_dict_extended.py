"""
Extended coverage for get_distances output branches not reached by
test_get_distances_extended.py:

- output_type='dictionary' with output_structure_indices='structure' (atom_indices_2=None)
- output_type='dictionary' with output_structure_indices='structure' (two systems)
- output_type='dictionary' with output_structure_indices='selection'
- output_type='dictionary' pairs=True with output_structure_indices set
- output_type='numpy.ndarray' with output_structure_indices='selection'
- output_type='numpy.ndarray' with output_indices='atom' and atom_indices_2=None
- weights parameter (center of atoms with explicit weights)
- Two-system distance with explicit structure_indices_2 → dictionary output
"""

import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import pytest


@pytest.fixture(scope='module')
def tctim():
    return msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')


@pytest.fixture(scope='module')
def pentalanine():
    return msm.convert(systems['pentalanine']['traj_pentalanine.h5msm'], to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# output_type='dictionary', output_structure_indices='structure', single system
# ---------------------------------------------------------------------------

def test_dict_atom_structure_indices_no_sel2(tctim):
    """dict output, output_indices='atom', output_structure_indices='structure', no sel2."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        output_type='dictionary',
        output_indices='atom',
        output_structure_indices='structure',
    )
    assert isinstance(result, dict)


def test_dict_selection_structure_indices_no_sel2(tctim):
    """dict output, output_indices='selection', output_structure_indices='structure', no sel2."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        output_type='dictionary',
        output_indices='selection',
        output_structure_indices='structure',
    )
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# output_type='dictionary', output_structure_indices='structure', two systems
# ---------------------------------------------------------------------------

def test_dict_atom_structure_indices_two_systems(tctim):
    """dict output, output_indices='atom', output_structure_indices='structure', sel2 given."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='dictionary',
        output_indices='atom',
        output_structure_indices='structure',
    )
    assert isinstance(result, dict)


def test_dict_selection_structure_indices_two_systems(tctim):
    """dict output, output_indices='selection', output_structure_indices='structure', sel2 given."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='dictionary',
        output_indices='selection',
        output_structure_indices='structure',
    )
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# output_type='dictionary', output_structure_indices='selection'
# ---------------------------------------------------------------------------

def test_dict_atom_structure_selection(tctim):
    """dict output, output_indices='atom', output_structure_indices='selection'."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='dictionary',
        output_indices='atom',
        output_structure_indices='selection',
    )
    assert isinstance(result, dict)


def test_dict_selection_structure_selection(tctim):
    """dict output, output_indices='selection', output_structure_indices='selection'."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='dictionary',
        output_indices='selection',
        output_structure_indices='selection',
    )
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# output_type='numpy.ndarray', output_structure_indices='selection'
# ---------------------------------------------------------------------------

def test_ndarray_structure_selection(tctim):
    """numpy output, output_structure_indices='selection' returns tuple with structure list."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='numpy.ndarray',
        output_structure_indices='selection',
    )
    assert isinstance(result, tuple)


# ---------------------------------------------------------------------------
# output_type='numpy.ndarray', output_indices='atom', atom_indices_2=None
# ---------------------------------------------------------------------------

def test_ndarray_atom_indices_no_sel2(tctim):
    """numpy output, output_indices='atom', no sel2 — uses sel1 for both dims."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        output_type='numpy.ndarray',
        output_indices='atom',
    )
    assert isinstance(result, tuple)
    assert len(result) == 2  # (atom_indices, distances)


def test_ndarray_selection_indices_no_sel2(tctim):
    """numpy output, output_indices='selection', no sel2."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        output_type='numpy.ndarray',
        output_indices='selection',
    )
    assert isinstance(result, tuple)


# ---------------------------------------------------------------------------
# weights parameter (center of atoms with explicit weights)
# ---------------------------------------------------------------------------

def test_weights_center_of_atoms(tctim):
    """center_of_atoms=True with explicit uniform weights."""
    n_atoms_in_group0 = msm.get(tctim, element='atom', selection='group_index==0', n_atoms=True)
    weights = np.ones(n_atoms_in_group0)
    dist_weighted = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        center_of_atoms=True,
        weights=weights,
        selection_2='group_index==1',
        center_of_atoms_2=True,
    )
    dist_plain = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        center_of_atoms=True,
        selection_2='group_index==1',
        center_of_atoms_2=True,
    )
    # Uniform weights should give the same result as unweighted
    assert np.allclose(
        puw.get_value(dist_weighted, to_unit='nm'),
        puw.get_value(dist_plain, to_unit='nm'),
        atol=1e-5,
    )


# ---------------------------------------------------------------------------
# Two systems with explicit structure_indices_2 → dict output
# ---------------------------------------------------------------------------

def test_two_systems_explicit_structure_indices_dict(pentalanine):
    """Two systems with explicit structure_indices_2 and dict output."""
    result = msm.structure.get_distances(
        pentalanine,
        selection='group_index==0',
        structure_indices=0,
        molecular_system_2=pentalanine,
        selection_2='group_index==4',
        structure_indices_2=1,
        output_type='dictionary',
        output_indices='atom',
        output_structure_indices='structure',
    )
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# pairs=True, output_type='dictionary', output_structure_indices set
# ---------------------------------------------------------------------------

def test_pairs_dict_structure_indices(tctim):
    """pairs=True with dict output and output_structure_indices='structure'."""
    pairs = np.array([[0, 1], [1, 2], [2, 3]])
    result = msm.structure.get_distances(
        tctim,
        selection=pairs,
        pairs=True,
        output_type='dictionary',
        output_indices='selection',
        output_structure_indices='structure',
    )
    assert isinstance(result, dict)


def test_pairs_dict_atom_structure_indices(tctim):
    """pairs=True, output_indices='atom', output_structure_indices='structure'."""
    pairs = np.array([[0, 1], [1, 2]])
    result = msm.structure.get_distances(
        tctim,
        selection=pairs,
        pairs=True,
        output_type='dictionary',
        output_indices='atom',
        output_structure_indices='structure',
    )
    assert isinstance(result, dict)
