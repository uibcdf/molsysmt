"""
Contract tests for openmm.GromacsGroFile form.

Oracle: gmx_coords.gro (5191 atoms, 1 frame, with periodic box vectors).
Secondary: md_1u19.gro (5547 atoms, 1 frame).

Covers:
- is_form
- to_molsysmt_Topology
- to_molsysmt_Structures
- to_molsysmt_MolSys
- get_structural_attributes: coordinates, box, n_structures, time, structure_id
"""

import pytest
from pathlib import Path
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


GRO_DIR = Path(msm.__file__).parent / 'data' / 'gro'
GMX_GRO = str(GRO_DIR / 'gmx_coords.gro')

N_ATOMS  = 5191
N_FRAMES = 1

openmm = pytest.importorskip('openmm')


@pytest.fixture(scope='module')
def gro_obj():
    """Raw openmm.GromacsGroFile object."""
    from openmm.app import GromacsGroFile
    return GromacsGroFile(GMX_GRO)


@pytest.fixture(scope='module')
def gro_topology(gro_obj):
    return msm.convert(gro_obj, to_form='molsysmt.Topology')


@pytest.fixture(scope='module')
def gro_molsys(gro_obj):
    return msm.convert(gro_obj, to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# is_form
# ---------------------------------------------------------------------------

def test_is_form(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import is_form
    assert is_form(gro_obj) is True


def test_is_form_false_for_string():
    from molsysmt.form.openmm_GromacsGroFile import is_form
    assert is_form('something.gro') is False


# ---------------------------------------------------------------------------
# Topology
# ---------------------------------------------------------------------------

def test_topology_atom_count(gro_topology):
    assert gro_topology.n_atoms == N_ATOMS


def test_topology_groups_positive(gro_topology):
    assert gro_topology.n_groups > 0


def test_topology_atom_names_not_empty(gro_topology):
    names = gro_topology.atoms['atom_name'].tolist()
    assert len(names) == N_ATOMS
    assert all(isinstance(n, str) for n in names)


# ---------------------------------------------------------------------------
# MolSys
# ---------------------------------------------------------------------------

def test_molsys_not_none(gro_molsys):
    assert gro_molsys is not None


def test_molsys_atom_count(gro_molsys):
    assert gro_molsys.topology.n_atoms == N_ATOMS


# ---------------------------------------------------------------------------
# Structural attributes via get_structural_attributes
# ---------------------------------------------------------------------------

def test_n_structures_all(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    n = gsa.get_n_structures_from_system(gro_obj, skip_digestion=True)
    assert n == N_FRAMES


def test_n_structures_explicit(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    n = gsa.get_n_structures_from_system(gro_obj, structure_indices=[0], skip_digestion=True)
    assert n == 1


def test_coordinates_shape(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    xyz = gsa.get_coordinates_from_atom(gro_obj, skip_digestion=True)
    val = puw.get_value(xyz)
    assert val.shape == (N_FRAMES, N_ATOMS, 3)


def test_coordinates_subset(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    xyz = gsa.get_coordinates_from_atom(gro_obj, indices=[0, 1, 2], skip_digestion=True)
    val = puw.get_value(xyz)
    assert val.shape == (N_FRAMES, 3, 3)


def test_coordinates_unit_nm(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    xyz = gsa.get_coordinates_from_atom(gro_obj, skip_digestion=True)
    unit_str = str(puw.get_unit(xyz))
    assert 'nm' in unit_str or 'nanometer' in unit_str


def test_box_not_none(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    box = gsa.get_box_from_system(gro_obj, skip_digestion=True)
    assert box is not None


def test_box_shape(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    box = gsa.get_box_from_system(gro_obj, skip_digestion=True)
    val = puw.get_value(box)
    assert val.shape == (N_FRAMES, 3, 3)


def test_time_is_none(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    t = gsa.get_time_from_system(gro_obj, skip_digestion=True)
    assert t is None


def test_structure_id_is_none(gro_obj):
    from molsysmt.form.openmm_GromacsGroFile import get_structural_attributes as gsa
    sid = gsa.get_structure_id_from_system(gro_obj, skip_digestion=True)
    assert sid is None
