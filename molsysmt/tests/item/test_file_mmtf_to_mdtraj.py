from molsysmt.item import file_mmtf
import mdtraj as mdt
import pytest


@pytest.fixture()
def mmtf_file_path():
    return "../../../data/mmtf/1sux.mmtf"


def test_load_mmtf(mmtf_file_path):

    traj = file_mmtf.load_mmtf(mmtf_file_path)
    assert traj.n_atoms == 4257


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

# Test for utilities functions


def test_is_int():

    assert file_mmtf.to_mdtraj._isint(str(10))
    assert file_mmtf.to_mdtraj._isint(str(-30))
    assert not file_mmtf.to_mdtraj._isint(str(20.0))


def test_is_float():

    assert file_mmtf.to_mdtraj._isfloat("10")
    assert file_mmtf.to_mdtraj._isfloat("-30.5")
    assert file_mmtf.to_mdtraj._isfloat("20.0532")
    assert file_mmtf.to_mdtraj._isfloat("10e20")
    assert file_mmtf.to_mdtraj._isfloat("15e-20")


def test_parse_gro_coord():
    line = "    0ACE    CH3    1   3.797   4.562   0.755 -0.8307  0.0927  0.6241"
    first_decimal = line.index('.', 20)
    second_decimal = line.index('.', first_decimal + 1)
    coords = file_mmtf.to_mdtraj._parse_gro_coord(line, first_decimal, second_decimal)
    assert coords == (3.797, 4.562, 0.755)

    line = "   10TYR     CA  131   3.497   3.865   2.048 -1.1193 -1.0588  0.0198"
    first_decimal = line.index('.', 20)
    second_decimal = line.index('.', first_decimal + 1)
    coords = file_mmtf.to_mdtraj._parse_gro_coord(line, first_decimal, second_decimal)
    assert coords == (3.497, 3.865, 2.048)


def test_is_gro_box():

    line = "    0ACE    CH3    1   3.797   4.562   0.755 -0.8307  0.0927  0.6241"
    assert not file_mmtf.to_mdtraj._is_gro_box(line)

    line = "   8.09204   8.09204   9.65194"
    assert file_mmtf.to_mdtraj._is_gro_box(line)
