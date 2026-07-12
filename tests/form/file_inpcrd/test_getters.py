"""
Getter tests for the file:inpcrd form.

The form declares n_atoms, n_structures, coordinates, velocities and box in its
`attributes.py`, but implemented none of the corresponding getters: every
`get_*_from_*` call fell through to a raw AttributeError. These tests pin the
implemented getters and the two behaviours that depended on them.

Oracle: the bundled pentalanine system (prmtop + inpcrd, 5207 atoms), plus
openmm.AmberInpcrdFile as the numerical source of truth for coordinates.
"""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt import systems
from molsysmt.form import _dict_modules


N_ATOMS = 5207


@pytest.fixture()
def inpcrd():
    return systems['pentalanine']['pentalanine.inpcrd']


@pytest.fixture()
def prmtop():
    return systems['pentalanine']['pentalanine.prmtop']


@pytest.fixture()
def tiny_inpcrd(tmp_path):
    """A well-formed inpcrd holding a different number of atoms (3)."""
    path = tmp_path / 'tiny.inpcrd'
    path.write_text(
        "TINY\n"
        "    3\n"
        "  1.0000000  0.0000000  0.0000000  2.0000000  0.0000000  0.0000000\n"
        "  3.0000000  0.0000000  0.0000000\n"
    )
    return str(path)


# ---------------------------------------------------------------------------
# Contract: every attribute declared as available has a working getter
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('getter', [
    'get_n_atoms_from_system',
    'get_n_structures_from_system',
    'get_coordinates_from_system',
    'get_velocities_from_system',
    'get_box_from_system',
    'get_box_shape_from_system',
    'get_box_lengths_from_system',
    'get_box_angles_from_system',
    'get_box_volume_from_system',
    'get_structure_id_from_system',
    'get_coordinates_from_atom',
    'get_velocities_from_atom',
])
def test_getter_is_implemented(getter):
    assert hasattr(_dict_modules['file:inpcrd'], getter)


# ---------------------------------------------------------------------------
# Regression: msm.get on an inpcrd used to raise a raw AttributeError
# ---------------------------------------------------------------------------

def test_get_n_atoms(inpcrd):
    assert msm.get(inpcrd, n_atoms=True) == N_ATOMS


def test_get_n_structures(inpcrd):
    assert msm.get(inpcrd, n_structures=True) == 1


def test_get_coordinates_shape(inpcrd):
    assert msm.get(inpcrd, coordinates=True).shape == (1, N_ATOMS, 3)


def test_get_box_shape(inpcrd):
    assert msm.get(inpcrd, box=True).shape == (1, 3, 3)


def test_get_velocities_is_none_when_file_has_none(inpcrd):
    # pentalanine.inpcrd carries no velocities; only restart files do
    assert msm.get(inpcrd, velocities=True) is None


# ---------------------------------------------------------------------------
# Parity: coordinates against openmm.AmberInpcrdFile
# ---------------------------------------------------------------------------

def test_parity_coordinates_with_openmm(inpcrd):
    from openmm.app import AmberInpcrdFile
    reference = np.array(puw.get_value(AmberInpcrdFile(inpcrd).getPositions(), to_unit='nm'))
    coordinates = puw.get_value(msm.get(inpcrd, coordinates=True)[0], to_unit='nm')
    assert np.allclose(coordinates, reference)


# ---------------------------------------------------------------------------
# The n_atoms getter is what lets a topology+coordinates pair be validated
# ---------------------------------------------------------------------------

def test_n_atoms_agrees_with_matching_prmtop(inpcrd, prmtop):
    assert msm.get(inpcrd, n_atoms=True) == msm.get(prmtop, n_atoms=True)


def test_matching_prmtop_and_inpcrd_are_one_molecular_system(prmtop, inpcrd):
    assert msm.basic.is_a_molecular_system([prmtop, inpcrd]) is True


def test_mismatched_prmtop_and_inpcrd_are_not_a_molecular_system(prmtop, tiny_inpcrd):
    # Without get_n_atoms_from_system the atom-count probe raised, the exception
    # was swallowed, and this pair was silently accepted as a valid system.
    assert msm.basic.is_a_molecular_system([prmtop, tiny_inpcrd]) is False
