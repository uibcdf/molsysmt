from molsysmt.item import file_mmtf
import mdtraj as mdt
import pytest


@pytest.fixture()
def mmtf_file_path():
    return "../../../data/mmtf/1sux.mmtf"


def test_load_mmtf(mmtf_file_path):

    traj = file_mmtf.load_mmtf(mmtf_file_path)
    assert traj.n_atoms == 4257
    assert traj.n_frames == 1
    assert traj.n_residues == 882


# Tests for MMTFTrajectoryFile class

def test_mmtf_trajectory_file_load_name_replacement_tables():

    residue_replacements, atom_replacements = file_mmtf.MMTFTrajectoryFile._load_name_replacement_tables()
    assert isinstance(residue_replacements, dict)
    assert isinstance(atom_replacements, dict)
    assert len(residue_replacements) == 62
    assert len(atom_replacements) == 40


def test_mmtf_trajectory_file_read_topology(mmtf_file_path):

    n_atoms, topology = file_mmtf.MMTFTrajectoryFile._read_topology(mmtf_file_path)
    assert isinstance(topology, mdt.Topology)
    assert n_atoms == 4257
    assert topology.n_atoms == 4257
    assert topology.n_residues == 882
    assert topology.n_chains == 12
    assert topology.n_bonds == 3949


def test_mmtf_trajectory_file_read_frame():
    pass


def test_mmtf_trajectory_write_frame_topology():
    pass


def test_mmtf_trajectory_file_read():
    pass


def test_mmtf_trajectory_file_read_as_traj():
    pass

