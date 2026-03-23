"""
Contract tests for MDAnalysis.Topology form.

MDAnalysis.Topology is the internal topology object inside an MDAnalysis
Universe.  It is created by parsing a PDB file via
msm.convert(pdb_path, to_form='MDAnalysis.Topology').

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, 20 residues, 1 chain).

Contract: MDAnalysis.Topology can be created and its native attributes
(n_atoms, n_residues, n_segments) match the expected oracle counts.

Note: msm.get() on MDAnalysis.Topology is not fully implemented; parity
tests use the MDAnalysis native API directly.
"""

import pytest
from pathlib import Path
import molsysmt as msm


PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')
N_ATOMS    = 304
N_RESIDUES = 20
N_SEGMENTS = 1


@pytest.fixture(scope='module')
def mda_topology():
    return msm.convert(PDB_PATH, to_form='MDAnalysis.Topology')


# ---------------------------------------------------------------------------
# Contract: MDAnalysis.Topology is created from a PDB file
# ---------------------------------------------------------------------------

def test_mda_topology_is_created(mda_topology):
    from MDAnalysis.core.topology import Topology
    assert isinstance(mda_topology, Topology)


def test_mda_topology_atom_count(mda_topology):
    assert mda_topology.n_atoms == N_ATOMS


def test_mda_topology_residue_count(mda_topology):
    assert mda_topology.n_residues == N_RESIDUES


def test_mda_topology_segment_count(mda_topology):
    assert mda_topology.n_segments == N_SEGMENTS


# ---------------------------------------------------------------------------
# Parity: MDAnalysis.Topology == source PDB (via native MDAnalysis API)
# ---------------------------------------------------------------------------

def test_parity_atom_names(mda_topology):
    source = msm.convert(PDB_PATH, to_form='MDAnalysis.Universe')
    assert list(mda_topology.names.values) == list(source._topology.names.values)


def test_parity_resnames(mda_topology):
    source = msm.convert(PDB_PATH, to_form='MDAnalysis.Universe')
    assert list(mda_topology.resnames.values) == list(source._topology.resnames.values)
