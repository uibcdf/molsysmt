"""
Contract and parity tests for MDAnalysis.AtomGroup form.

MDAnalysis.AtomGroup is a selection/view of a Universe.  The canonical way
to obtain one is Universe.select_atoms().

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, 20 residues, 1 chain).
Contract: An AtomGroup covering all atoms can be converted to
molsysmt.Topology.
Parity: AtomGroup topology == parent Universe topology (same counts and
names).
"""

import pytest
from pathlib import Path
import molsysmt as msm


PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')
N_ATOMS  = 304
N_GROUPS = 20
N_CHAINS = 1


@pytest.fixture(scope='module')
def atom_group():
    universe = msm.convert(PDB_PATH, to_form='MDAnalysis.Universe')
    return universe.select_atoms('all')


@pytest.fixture(scope='module')
def atomgroup_topology(atom_group):
    return msm.convert(atom_group, to_form='molsysmt.Topology')


@pytest.fixture(scope='module')
def source_topology():
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: AtomGroup can be converted to molsysmt.Topology
# ---------------------------------------------------------------------------

def test_atomgroup_is_created(atom_group):
    import MDAnalysis as mda
    assert isinstance(atom_group, mda.core.groups.AtomGroup)


def test_atomgroup_topology_atom_count(atomgroup_topology):
    assert atomgroup_topology.n_atoms == N_ATOMS


def test_atomgroup_topology_group_count(atomgroup_topology):
    assert atomgroup_topology.n_groups == N_GROUPS


def test_atomgroup_topology_chain_count(atomgroup_topology):
    assert atomgroup_topology.n_chains == N_CHAINS


# ---------------------------------------------------------------------------
# Parity: AtomGroup topology == source PDB topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(atomgroup_topology, source_topology):
    assert atomgroup_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(atomgroup_topology, source_topology):
    assert atomgroup_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(atomgroup_topology, source_topology):
    assert atomgroup_topology.n_chains == source_topology.n_chains


def test_parity_atom_names(atomgroup_topology, source_topology):
    assert atomgroup_topology.atoms['atom_name'].tolist() == source_topology.atoms['atom_name'].tolist()


def test_parity_group_names(atomgroup_topology, source_topology):
    assert atomgroup_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()
