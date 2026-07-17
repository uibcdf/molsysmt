"""
Contract and parity tests for MDAnalysis.Universe form.

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, 20 residues, 1 chain).
Chosen because it is a single-chain, single-model structure that MDAnalysis
reads without chain-merging artefacts.

Contract: MDAnalysis.Universe can be created from a PDB file and converted
to molsysmt.Topology.
Parity: Universe topology == source PDB topology (atom count, group count,
chain count, atom names, group names).
"""

import pytest
import warnings
from pathlib import Path
import molsysmt as msm


PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')
N_ATOMS  = 304
N_GROUPS = 20
N_CHAINS = 1


@pytest.fixture(scope='module')
def universe():
    return msm.convert(PDB_PATH, to_form='MDAnalysis.Universe')


@pytest.fixture(scope='module')
def universe_topology(universe):
    return msm.convert(universe, to_form='molsysmt.Topology')


@pytest.fixture(scope='module')
def source_topology():
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: MDAnalysis.Universe can be created and converted to Topology
# ---------------------------------------------------------------------------

def test_universe_is_created(universe):
    import MDAnalysis as mda
    assert isinstance(universe, mda.Universe)


def test_universe_topology_atom_count(universe_topology):
    assert universe_topology.n_atoms == N_ATOMS


def test_universe_topology_group_count(universe_topology):
    assert universe_topology.n_groups == N_GROUPS


def test_universe_topology_chain_count(universe_topology):
    assert universe_topology.n_chains == N_CHAINS


# ---------------------------------------------------------------------------
# Parity: MDAnalysis.Universe topology == source PDB topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(universe_topology, source_topology):
    assert universe_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(universe_topology, source_topology):
    assert universe_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(universe_topology, source_topology):
    assert universe_topology.n_chains == source_topology.n_chains


def test_parity_atom_names(universe_topology, source_topology):
    assert universe_topology.atoms['atom_name'].tolist() == source_topology.atoms['atom_name'].tolist()


def test_parity_group_names(universe_topology, source_topology):
    assert universe_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()


def test_pdb_universe_does_not_invent_time(universe):
    with warnings.catch_warnings():
        warnings.simplefilter('error', UserWarning)
        assert msm.get(universe, element='system', time=True) is None
