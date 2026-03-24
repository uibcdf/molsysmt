"""
Unit and regression test for the get_contacts module of the molsysmt package on XYZ molecular
systems (particles 4 geometry fixture).

Covered branches
----------------
- pairs=True with iterable-of-pairs selection (lines 95-99)
- output_type='pairs' with pairs=True and output_indices='selection' (lines 144-147)
- output_type='pairs' with pairs=True and output_indices='atom' (lines 148-151)
- output_type='pairs' with pairs=False and selection_2 provided (lines 161-164)
- output_type='pairs' with output_indices='atom' and selection_2 provided (lines 168-178)
- output_type='sorted pairs' (lines 181-182)

Geometry (particles 4, nm)
--------------------------
frame 0: [[0,2,-1],[-1,1,1],[-2,0,1],[-2,-2,-2]]
frame 1: [[1,2,-1],[-1,0,1],[-2,0,0],[0,0,0]]
frame 2: [[0,2,-1],[0,0,1],[-1,1,0],[2,2,2]]
"""

import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np


def _make_molsys():
    return msm.convert(systems['particles 4']['traj_particles_4.xyznpy'], to_form='XYZ')


# ---------------------------------------------------------------------------
# pairs=True with an iterable-of-pairs selection (lines 95-99)
# ---------------------------------------------------------------------------

def test_get_contacts_from_XYZ_pairs_iterable_of_pairs_shape():
    """pairs=True + list-of-pairs: result shape is (n_structures, n_pairs)."""
    molsys = _make_molsys()
    contact_map = msm.structure.get_contacts(
        molsys,
        selection=[[0, 2], [1, 3]],
        threshold='3 nm',
        pairs=True,
    )
    assert contact_map.shape == (3, 2)


def test_get_contacts_from_XYZ_pairs_iterable_of_pairs_values():
    """pairs=True + list-of-pairs: correct boolean values per frame."""
    molsys = _make_molsys()
    contact_map = msm.structure.get_contacts(
        molsys,
        selection=[[0, 2], [1, 3]],
        threshold='3 nm',
        pairs=True,
    )
    # frame 0: d(0,2)=sqrt(12)~3.46>3 → False; d(1,3)=sqrt(19)~4.36>3 → False
    assert np.array_equal(contact_map[0], [False, False])
    # frame 1: d(0,2)=sqrt(14)~3.74>3 → False; d(1,3)=sqrt(2)~1.41<=3 → True
    assert np.array_equal(contact_map[1], [False, True])
    # frame 2: d(0,2)=sqrt(3)~1.73<=3 → True; d(1,3)=3.0<=3 → True
    assert np.array_equal(contact_map[2], [True, True])


# ---------------------------------------------------------------------------
# output_type='pairs', pairs=True, output_indices='selection' (lines 144-147)
# ---------------------------------------------------------------------------

def test_get_contacts_from_XYZ_output_pairs_pairs_selection_indices():
    """output_type='pairs' + pairs=True + output_indices='selection': list of pair-position indices."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection=[[0, 2], [1, 3]],
        threshold='3 nm',
        pairs=True,
        output_type='pairs',
        output_indices='selection',
    )
    # 3 frames; each entry is the list of pair-positions (0-based) that are in contact
    assert len(output) == 3
    # frame 0: no contacts
    assert output[0] == []
    # frame 1: only pair index 1 (atoms 1,3) is in contact
    assert output[1] == [1]
    # frame 2: both pair indices 0 (atoms 0,2) and 1 (atoms 1,3) are in contact
    assert output[2] == [0, 1]


# ---------------------------------------------------------------------------
# output_type='pairs', pairs=True, output_indices='atom' (lines 148-151)
# ---------------------------------------------------------------------------

def test_get_contacts_from_XYZ_output_pairs_pairs_atom_indices():
    """output_type='pairs' + pairs=True + output_indices='atom': list of [atom_i, atom_j] pairs."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection=[[0, 2], [1, 3]],
        threshold='3 nm',
        pairs=True,
        output_type='pairs',
        output_indices='atom',
    )
    assert len(output) == 3
    # frame 0: no contacts
    assert output[0] == []
    # frame 1: pair (atoms 1,3) is in contact
    assert output[1] == [[1, 3]]
    # frame 2: pairs (atoms 0,2) and (atoms 1,3) are in contact
    assert output[2] == [[0, 2], [1, 3]]


# ---------------------------------------------------------------------------
# output_type='pairs', pairs=False, selection_2 provided (lines 161-164)
# ---------------------------------------------------------------------------

def test_get_contacts_from_XYZ_output_pairs_two_selections_selection_indices():
    """output_type='pairs' + selection_2 provided: default (None) positional indices."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection=[0, 1],
        selection_2=[2, 3],
        threshold='2 nm',
        output_type='pairs',
        structure_indices=[1],
    )
    # frame 1 only: contact matrix is (2,2); d(0,2)~3.74, d(0,3)~2.45 → False;
    # d(1,2)~1.41, d(1,3)~1.41 → True
    # nonzero of [[False,False],[True,True]] → rows=[1,1], cols=[0,1]
    assert len(output) == 1
    assert output[0] == [[1, 0], [1, 1]]


def test_get_contacts_from_XYZ_output_pairs_two_selections_atom_indices():
    """output_type='pairs' + selection_2 + output_indices='atom': global atom indices."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection=[0, 1],
        selection_2=[2, 3],
        threshold='2 nm',
        output_type='pairs',
        output_indices='atom',
        structure_indices=[1],
    )
    # row=1 maps to atom_indices[1]=1; col=0 maps to atom_indices_2[0]=2
    # row=1 maps to atom_indices[1]=1; col=1 maps to atom_indices_2[1]=3
    assert len(output) == 1
    assert output[0] == [[1, 2], [1, 3]]


# ---------------------------------------------------------------------------
# output_type='pairs', pairs=False, no selection_2 (lines 155-159 already
# partially covered by existing tests; here we exercise output_indices='atom')
# ---------------------------------------------------------------------------

def test_get_contacts_from_XYZ_output_pairs_no_sel2_atom_indices():
    """output_type='pairs' + no selection_2 + output_indices='atom': atom indices in upper triangle."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection='all',
        threshold='2 nm',
        output_type='pairs',
        output_indices='atom',
        structure_indices=[1],
    )
    # frame 1 upper-triangle contacts (threshold 2 nm):
    # d(1,2)~1.41 → True; d(1,3)~1.41 → True; d(2,3)=2.0 → True
    # positional pairs: (1,2),(1,3),(2,3) — these ARE the atom indices for 4-particle XYZ
    assert len(output) == 1
    assert output[0] == [[1, 2], [1, 3], [2, 3]]


# ---------------------------------------------------------------------------
# output_type='pairs', no output_indices (raw positional), no selection_2
# ---------------------------------------------------------------------------

def test_get_contacts_from_XYZ_output_pairs_no_sel2_raw():
    """output_type='pairs', no selection_2, no output_indices: positional upper-triangle pairs."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection='all',
        threshold='2 nm',
        output_type='pairs',
        structure_indices=[1],
    )
    assert len(output) == 1
    assert output[0] == [[1, 2], [1, 3], [2, 3]]


# ---------------------------------------------------------------------------
# output_type='sorted pairs' (lines 181-182)
# ---------------------------------------------------------------------------

def test_get_contacts_from_XYZ_output_sorted_pairs():
    """output_type='sorted pairs': same as 'pairs' but each frame's list is sorted."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection='all',
        threshold='2 nm',
        output_type='sorted pairs',
        structure_indices=[1],
    )
    assert len(output) == 1
    # sorted([[1,2],[1,3],[2,3]]) == [[1,2],[1,3],[2,3]] (already sorted)
    assert output[0] == sorted([[1, 2], [1, 3], [2, 3]])


def test_get_contacts_from_XYZ_output_sorted_pairs_multiple_frames():
    """output_type='sorted pairs' with multiple frames returns a sorted list per frame."""
    molsys = _make_molsys()
    output = msm.structure.get_contacts(
        molsys,
        selection='all',
        threshold='2 nm',
        output_type='sorted pairs',
    )
    assert len(output) == 3
    for frame_pairs in output:
        assert frame_pairs == sorted(frame_pairs)
