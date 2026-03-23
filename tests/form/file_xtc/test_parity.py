"""
Parity tests for file:xtc form.

Oracle: builder_trajectory_molsys (4 atoms, 3 frames).
The same 3-frame trajectory is persisted in both file:h5msm (topology +
structures) and file:xtc (structures only, written via mdtraj).

Parity means that loading the XTC file (structures) and combining it with
the h5msm topology gives coordinates that are numerically identical to the
h5msm source on all frames.

XTC stores coordinates as float32 (nanometer precision ~1e-3 nm), so the
tolerance for coordinate comparison is set at 1e-3 nm.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


XTC_RTOL = 1e-3   # XTC float32 precision in nm


@pytest.fixture()
def source_structures(builder_trajectory_molsys):
    return builder_trajectory_molsys.structures


@pytest.fixture()
def xtc_structures(builder_trajectory_xtc_file):
    return msm.convert(builder_trajectory_xtc_file, to_form='molsysmt.Structures',
                       structure_indices='all')


# ---------------------------------------------------------------------------
# Contract: file:xtc can be loaded as molsysmt.Structures
# ---------------------------------------------------------------------------

def test_xtc_loads_as_structures(xtc_structures):
    assert xtc_structures is not None


def test_xtc_frame_count(xtc_structures, source_structures):
    assert xtc_structures.n_structures == source_structures.n_structures


def test_xtc_atom_count(xtc_structures, source_structures):
    assert xtc_structures.n_atoms == source_structures.n_atoms


# ---------------------------------------------------------------------------
# Parity: XTC coordinates ↔ h5msm source (within float32 tolerance)
# ---------------------------------------------------------------------------

def test_parity_coordinates_all_frames(xtc_structures, source_structures):
    xtc_coords = puw.get_value(xtc_structures.coordinates, to_unit='nm')
    src_coords = puw.get_value(source_structures.coordinates, to_unit='nm')
    assert np.allclose(xtc_coords, src_coords, atol=XTC_RTOL)


def test_parity_frame0_coordinates(xtc_structures, source_structures):
    xtc_f0 = puw.get_value(xtc_structures.coordinates[0], to_unit='nm')
    src_f0 = puw.get_value(source_structures.coordinates[0], to_unit='nm')
    assert np.allclose(xtc_f0, src_f0, atol=XTC_RTOL)


def test_parity_frame1_coordinates(xtc_structures, source_structures):
    xtc_f1 = puw.get_value(xtc_structures.coordinates[1], to_unit='nm')
    src_f1 = puw.get_value(source_structures.coordinates[1], to_unit='nm')
    assert np.allclose(xtc_f1, src_f1, atol=XTC_RTOL)


def test_parity_frame2_coordinates(xtc_structures, source_structures):
    xtc_f2 = puw.get_value(xtc_structures.coordinates[2], to_unit='nm')
    src_f2 = puw.get_value(source_structures.coordinates[2], to_unit='nm')
    assert np.allclose(xtc_f2, src_f2, atol=XTC_RTOL)
