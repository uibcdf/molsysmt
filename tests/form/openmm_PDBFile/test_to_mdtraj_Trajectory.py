"""Check the OpenMM PDBFile to MDTraj trajectory conversion."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form.openmm_PDBFile.to_mdtraj_Trajectory import to_mdtraj_Trajectory


def test_selected_atoms_keep_their_coordinates():
    """The topology and coordinates use the same selected atom order."""
    pytest.importorskip("mdtraj")
    openmm_app = pytest.importorskip("openmm.app")
    pdb_path = Path(msm.__file__).parent / "data" / "pdb" / "1l2y.pdb"
    source = openmm_app.PDBFile(str(pdb_path))
    atom_indices = [0, 2, 4]

    trajectory = to_mdtraj_Trajectory(source, atom_indices=atom_indices)

    expected = np.array(
        [
            msm.pyunitwizard.get_value(source.getPositions(frame=index), to_unit="nm")
            for index in range(source.getNumFrames())
        ]
    )
    assert trajectory.n_frames == source.getNumFrames() == 38
    assert trajectory.n_atoms == len(atom_indices)
    np.testing.assert_array_equal(
        trajectory.xyz, expected[:, atom_indices].astype("float32")
    )
