from types import SimpleNamespace

import numpy as np

from molsysmt.form.mdtraj_AmberRestartFile.get_topological_attributes import (
    get_atom_index_from_atom as get_amber_restart_atom_index,
)
from molsysmt.form.mdtraj_GroTrajectoryFile.get_topological_attributes import (
    get_atom_index_from_atom as get_gro_atom_index,
    get_n_atoms_from_system as get_gro_n_atoms,
)
from molsysmt.form.mdtraj_PDBTrajectoryFile.get_topological_attributes import (
    get_atom_index_from_atom as get_pdb_trajectory_atom_index,
)
from molsysmt.form.openmm_AmberInpcrdFile.get_topological_attributes import (
    get_atom_index_from_atom as get_openmm_inpcrd_atom_index,
)


class _FakeGroFile:

    def seek(self, position):
        assert position == 0


class _FakeGroTrajectory:

    def __init__(self, n_atoms):
        self._file = _FakeGroFile()
        self._coordinates = np.zeros((2, n_atoms, 3))

    def read(self):
        return self._coordinates, None, None


def test_amber_restart_atom_indices_follow_coordinate_width():
    item = SimpleNamespace(_n_atoms=4)

    assert get_amber_restart_atom_index(item, skip_digestion=True) == [0, 1, 2, 3]
    assert get_amber_restart_atom_index(item, indices=[3, 1], skip_digestion=True) == [3, 1]


def test_gro_atom_indices_and_count_follow_coordinate_width():
    item = _FakeGroTrajectory(n_atoms=5)

    assert get_gro_n_atoms(item, skip_digestion=True) == 5
    assert get_gro_atom_index(item, skip_digestion=True) == [0, 1, 2, 3, 4]


def test_pdb_trajectory_atom_indices_follow_topology():
    item = SimpleNamespace(topology=SimpleNamespace(n_atoms=3))

    assert get_pdb_trajectory_atom_index(item, skip_digestion=True) == [0, 1, 2]


def test_openmm_inpcrd_atom_indices_follow_reported_count():
    item = SimpleNamespace(getNumAtoms=lambda: 3)

    assert get_openmm_inpcrd_atom_index(item, skip_digestion=True) == [0, 1, 2]
