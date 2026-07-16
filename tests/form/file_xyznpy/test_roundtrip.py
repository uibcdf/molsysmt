"""
Contract and parity tests for file:xyznpy form.

file:xyznpy stores coordinate arrays as NumPy binary files (coordinates only,
no topology).  The round-trip path is:
  molsysmt.Structures → XYZ → file:xyznpy → XYZ → molsysmt.Structures

Oracle: builder_pdb_molsys (4 atoms, 1 frame).
Parity: coordinates are preserved exactly through the XYZ ↔ xyznpy roundtrip.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture()
def xyznpy_file(builder_pdb_molsys, tmp_path):
    path = str(tmp_path / 'builder.xyznpy')
    xyz = msm.convert(builder_pdb_molsys.structures, to_form='XYZ')
    msm.convert(xyz, to_form='file:xyznpy', output_filename=path)
    return path


@pytest.fixture()
def source_xyz(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys.structures, to_form='XYZ')


# ---------------------------------------------------------------------------
# Contract: file:xyznpy can be written and read back as XYZ
# ---------------------------------------------------------------------------

def test_xyznpy_file_is_created(xyznpy_file):
    import os
    assert os.path.isfile(xyznpy_file)


def test_xyznpy_loads_as_xyz(xyznpy_file):
    xyz = msm.convert(xyznpy_file, to_form='XYZ')
    assert xyz is not None


# ---------------------------------------------------------------------------
# Parity: file:xyznpy ↔ XYZ coordinates are preserved exactly
# ---------------------------------------------------------------------------

def test_parity_shape(xyznpy_file, source_xyz):
    xyz_back = msm.convert(xyznpy_file, to_form='XYZ')
    assert puw.get_value(xyz_back, to_unit='nm').shape == puw.get_value(source_xyz, to_unit='nm').shape


def test_parity_coordinates(xyznpy_file, source_xyz):
    xyz_back = msm.convert(xyznpy_file, to_form='XYZ')
    back = puw.get_value(xyz_back, to_unit='nm')
    orig = puw.get_value(source_xyz, to_unit='nm')
    assert np.allclose(back, orig)


def test_get_coordinates_from_atoms_with_subsets(xyznpy_file, source_xyz):
    output = msm.get(
        xyznpy_file,
        element='atom',
        selection=[0, 2],
        structure_indices=[0],
        coordinates=True,
    )

    observed = puw.get_value(output, to_unit='nm')
    expected = puw.get_value(source_xyz, to_unit='nm')[np.ix_([0], [0, 2])]
    assert np.allclose(observed, expected)


def test_get_coordinates_from_system(xyznpy_file, source_xyz):
    output = msm.get(
        xyznpy_file,
        element='system',
        structure_indices=[0],
        coordinates=True,
    )

    observed = puw.get_value(output, to_unit='nm')
    expected = puw.get_value(source_xyz, to_unit='nm')[[0], :, :]
    assert np.allclose(observed, expected)


def test_get_coordinates_returns_none_for_none_indices(xyznpy_file):
    output = msm.get(
        xyznpy_file,
        element='atom',
        selection=None,
        coordinates=True,
    )

    assert output is None
