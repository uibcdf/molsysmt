"""
Contract and parity tests for XYZ form.

XYZ is a coordinate-only in-memory form (pint.Quantity array of shape
(n_structures, n_atoms, 3), in nm).  It carries no topology.

The round-trip path is:
  molsysmt.Structures → XYZ → molsysmt.Structures

Oracle: builder_pdb_molsys (4 atoms, 1 frame).
Parity: coordinates are preserved exactly through the XYZ roundtrip.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture()
def source_structures(builder_pdb_molsys):
    return builder_pdb_molsys.structures


@pytest.fixture()
def xyz(source_structures):
    return msm.convert(source_structures, to_form='XYZ')


@pytest.fixture()
def roundtrip_structures(xyz):
    return msm.convert(xyz, to_form='molsysmt.Structures')


# ---------------------------------------------------------------------------
# Contract: XYZ is a pint.Quantity with the right shape
# ---------------------------------------------------------------------------

def test_xyz_is_quantity(xyz):
    import pint
    assert isinstance(xyz, pint.Quantity)


def test_xyz_shape(xyz):
    arr = puw.get_value(xyz, to_unit='nm')
    assert arr.shape == (1, 4, 3)   # (n_structures, n_atoms, 3)


# ---------------------------------------------------------------------------
# Parity: Structures → XYZ → Structures preserves coordinates
# ---------------------------------------------------------------------------

def test_parity_atom_count(roundtrip_structures, source_structures):
    assert roundtrip_structures.n_atoms == source_structures.n_atoms


def test_parity_structure_count(roundtrip_structures, source_structures):
    assert roundtrip_structures.n_structures == source_structures.n_structures


def test_parity_coordinates(roundtrip_structures, source_structures):
    back = puw.get_value(roundtrip_structures.coordinates, to_unit='nm')
    orig = puw.get_value(source_structures.coordinates, to_unit='nm')
    assert np.allclose(back, orig)
