"""Testing cursor-safe fidelity of MDTraj HDF5 reader objects."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


mdtraj = pytest.importorskip("mdtraj")


def test_hdf5_reader_getters_preserve_cursor_and_metadata():
    path = msm.systems["pentalanine"]["traj_pentalanine.h5"]
    structure_indices = [12, 1, 4000]
    with mdtraj.open(str(path)) as reader:
        reader.seek(9)
        output = msm.get(
            reader,
            element="system",
            structure_indices=structure_indices,
            time=True,
            temperature=True,
            kinetic_energy=True,
            potential_energy=True,
            total_energy=True,
            output_type="dictionary",
        )
        assert reader.tell() == 9

    assert puw.get_value(output["time"], to_unit="ps").shape == (3,)
    assert puw.get_value(output["temperature"], to_unit="K").shape == (3,)
    np.testing.assert_allclose(
        puw.get_value(output["total_energy"], to_unit="kJ/mol"),
        puw.get_value(output["kinetic_energy"], to_unit="kJ/mol")
        + puw.get_value(output["potential_energy"], to_unit="kJ/mol"),
    )


def test_hdf5_reader_native_conversion_preserves_available_fields_and_cursor():
    path = msm.systems["pentalanine"]["traj_pentalanine.h5"]
    with mdtraj.open(str(path)) as reader:
        reader.seek(11)
        output = msm.convert(
            reader,
            to_form="molsysmt.MolSys",
            selection=[4, 1, 8],
            structure_indices=[7, 2],
        )
        assert reader.tell() == 11

    assert output.topology.n_atoms == 3
    assert output.structures.coordinates.shape == (2, 3, 3)
    assert output.structures.time.shape == (2,)
    assert output.structures.temperature.shape == (2,)
    assert output.structures.kinetic_energy.shape == (2,)
    assert output.structures.potential_energy.shape == (2,)
    assert output.structures.velocities is None
