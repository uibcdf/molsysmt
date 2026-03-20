"""
Extended tests for molsysmt.structure.get_distances covering uncovered branches:
- pairs=True with explicit pair arrays
- molecular_system_2 (two-system distances)
- output_type='dictionary' with output_indices='atom'
- output_type='dictionary' with output_indices='selection'
- output_type='dictionary' with pairs=True
- output_structure_indices='structure'
- pbc=False path
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
    return msm.convert(systems['pentalanine']['pentalanine.h5msm'], to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# pairs=True
# ---------------------------------------------------------------------------

def test_pairs_as_array(tctim):
    """pairs=True with explicit 2-column array of atom indices."""
    pairs = np.array([[0, 1], [0, 2], [1, 2]])
    dist = msm.structure.get_distances(tctim, selection=pairs, pairs=True)
    assert dist.shape == (1, 3)
    assert np.all(puw.get_value(dist, to_unit='nm') >= 0)


def test_pairs_as_two_element_list(tctim):
    """pairs=True with a 2-element [sel1, sel2] list."""
    dist = msm.structure.get_distances(tctim, selection=['atom_index==0', 'atom_index==1'], pairs=True)
    assert dist.shape[0] == 1


# ---------------------------------------------------------------------------
# molecular_system_2
# ---------------------------------------------------------------------------

def test_two_systems(tctim):
    """Distances between two systems."""
    dist = msm.structure.get_distances(
        tctim, selection='group_index==0',
        molecular_system_2=tctim, selection_2='group_index==1'
    )
    assert dist.ndim == 3
    assert dist.shape[0] == 1


def test_two_systems_no_selection2(tctim):
    """molecular_system_2 with selection_2=None uses selection from system_1."""
    dist = msm.structure.get_distances(
        tctim, selection='group_index==0',
        molecular_system_2=tctim
    )
    assert dist.ndim == 3


# ---------------------------------------------------------------------------
# pbc=False
# ---------------------------------------------------------------------------

def test_pbc_false(tctim):
    """pbc=False bypasses PBC correction."""
    dist = msm.structure.get_distances(tctim, selection='group_index==0',
                                       selection_2='group_index==1', pbc=False)
    assert dist.ndim == 3
    assert np.all(puw.get_value(dist, to_unit='nm') >= 0)


# ---------------------------------------------------------------------------
# output_type='dictionary', output_indices='atom'
# ---------------------------------------------------------------------------

def test_output_dict_atom_indices(tctim):
    """output_type='dictionary', output_indices='atom' returns a dict."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='dictionary',
        output_indices='atom'
    )
    assert isinstance(result, dict)


def test_output_dict_atom_indices_with_structure(tctim):
    """output_type='dictionary', output_indices='atom', output_structure_indices='structure'."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='dictionary',
        output_indices='atom',
        output_structure_indices='structure'
    )
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# output_type='dictionary', output_indices='selection'
# ---------------------------------------------------------------------------

def test_output_dict_selection_indices(tctim):
    """output_type='dictionary', output_indices='selection' returns a dict."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='dictionary',
        output_indices='selection'
    )
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# output_type='numpy.ndarray', output_indices='atom'
# ---------------------------------------------------------------------------

def test_output_ndarray_atom_indices(tctim):
    """output_indices='atom' returns tuple (indices1, indices2, distances)."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='numpy.ndarray',
        output_indices='atom'
    )
    assert isinstance(result, tuple)
    assert len(result) == 3  # atom_indices, atom_indices_2, distances


def test_output_ndarray_selection_indices(tctim):
    """output_indices='selection' returns tuple (sel_indices, sel_indices_2, distances)."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='numpy.ndarray',
        output_indices='selection'
    )
    assert isinstance(result, tuple)


def test_output_ndarray_structure_indices(tctim):
    """output_structure_indices='structure' appends structure index list to output."""
    result = msm.structure.get_distances(
        tctim,
        selection='group_index==0',
        selection_2='group_index==1',
        output_type='numpy.ndarray',
        output_structure_indices='structure'
    )
    assert isinstance(result, tuple)


# ---------------------------------------------------------------------------
# output_type='dictionary', pairs=True
# ---------------------------------------------------------------------------

def test_output_dict_pairs(tctim):
    """output_type='dictionary' with pairs=True, output_indices='atom'."""
    pairs = np.array([[0, 1], [1, 2]])
    result = msm.structure.get_distances(
        tctim,
        selection=pairs,
        pairs=True,
        output_type='dictionary',
        output_indices='atom'
    )
    assert isinstance(result, dict)
