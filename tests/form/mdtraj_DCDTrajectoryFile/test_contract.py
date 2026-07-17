"""Testing cursor-safe access to MDTraj DCD readers."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


mdtraj = pytest.importorskip("mdtraj")
DCD_PATH = Path(msm.__file__).parent / "data" / "dcd" / "traj_chicken_villin_HP35_solvated.dcd"


def test_dcd_getters_preserve_cursor_and_support_subsets():
    with mdtraj.formats.DCDTrajectoryFile(str(DCD_PATH), mode="r") as reader:
        reader.seek(0)
        expected = reader.read(atom_indices=[3, 8])[0][[1, 9, 2]]
        reader.seek(6)
        coordinates = msm.get(
            reader,
            element="atom",
            selection=[3, 8],
            structure_indices=[1, 9, 2],
            coordinates=True,
        )
        box = msm.get(
            reader,
            element="system",
            structure_indices=[1, 9, 2],
            box=True,
        )
        n_atoms = msm.get(reader, element="system", n_atoms=True)

        assert reader.tell() == 6

    assert n_atoms == 4369
    assert puw.get_value(coordinates, to_unit="nm").shape == (3, 2, 3)
    assert puw.get_value(box, to_unit="nm").shape == (3, 3, 3)
    np.testing.assert_allclose(
        puw.get_value(coordinates, to_unit="angstrom"),
        expected,
        rtol=0.0,
        atol=3.0e-6,
    )


def test_dcd_conversion_preserves_cursor_and_frame_identity():
    with mdtraj.formats.DCDTrajectoryFile(str(DCD_PATH), mode="r") as reader:
        reader.seek(4)
        structures = msm.convert(
            reader,
            to_form="molsysmt.Structures",
            selection=[0, 2],
            structure_indices=[8, 1],
        )
        assert reader.tell() == 4

    assert structures.coordinates.shape == (2, 2, 3)
    np.testing.assert_array_equal(structures.structure_id, [8, 1])
