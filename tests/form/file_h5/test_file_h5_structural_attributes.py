"""Regression tests for structural attributes in MDTraj HDF5 files."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import systems


md = pytest.importorskip("mdtraj")


def _values(quantity, unit):
    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def test_coordinates_support_atom_and_structure_subsets():
    path = systems["pentalanine"]["traj_pentalanine.h5"]
    atom_indices = [4, 6, 8, 14]
    structure_indices = [0, 1000, 4999]
    expected = md.load(str(path)).xyz[structure_indices][:, atom_indices, :]

    observed = msm.get(
        path,
        element="atom",
        selection=atom_indices,
        structure_indices=structure_indices,
        coordinates=True,
    )

    assert _values(observed, "nm").shape == (3, 4, 3)
    np.testing.assert_allclose(_values(observed, "nm"), expected, rtol=0.0, atol=1.0e-7)


def test_frame_metadata_matches_mdtraj_hdf5_fields():
    path = systems["pentalanine"]["traj_pentalanine.h5"]
    structure_indices = [0, 2500, 4999]
    with md.open(str(path)) as handle:
        frames = handle.read()

    observed = msm.get(
        path,
        element="system",
        structure_indices=structure_indices,
        time=True,
        box=True,
        temperature=True,
        kinetic_energy=True,
        potential_energy=True,
        total_energy=True,
        output_type="dictionary",
    )

    np.testing.assert_allclose(
        _values(observed["time"], "ps"),
        frames.time[structure_indices],
        rtol=0.0,
        atol=1.0e-7,
    )
    np.testing.assert_allclose(
        _values(observed["temperature"], "K"),
        frames.temperature[structure_indices],
        rtol=0.0,
        atol=1.0e-6,
    )
    np.testing.assert_allclose(
        _values(observed["kinetic_energy"], "kJ/mol"),
        frames.kineticEnergy[structure_indices],
        rtol=0.0,
        atol=1.0e-5,
    )
    np.testing.assert_allclose(
        _values(observed["potential_energy"], "kJ/mol"),
        frames.potentialEnergy[structure_indices],
        rtol=0.0,
        atol=1.0e-5,
    )
    np.testing.assert_allclose(
        _values(observed["total_energy"], "kJ/mol"),
        frames.kineticEnergy[structure_indices] + frames.potentialEnergy[structure_indices],
        rtol=0.0,
        atol=1.0e-5,
    )
    assert _values(observed["box"], "nm").shape == (3, 3, 3)
