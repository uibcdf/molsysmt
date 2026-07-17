"""
Contract and parity tests for MDAnalysis.Topology form.

MDAnalysis.Topology is the internal topology object inside an MDAnalysis
Universe.  It is created by parsing a PDB file via
msm.convert(pdb_path, to_form='MDAnalysis.Topology').

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, 20 residues, 1 chain).

Contract: MDAnalysis.Topology can be created and its native attributes
(n_atoms, n_residues, n_segments) match the expected oracle counts.

Parity: MDAnalysis.Topology → molsysmt.Topology preserves atom count,
group count, chain count, atom names, and group names.
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


@pytest.fixture(scope='module')
def source_topology():
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')


@pytest.fixture(scope='module')
def roundtrip_topology(mda_topology):
    return msm.convert(mda_topology, to_form='molsysmt.Topology')


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
# Parity: MDAnalysis.Topology → molsysmt.Topology preserves topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_chains == source_topology.n_chains


def test_parity_atom_names(roundtrip_topology, source_topology):
    assert roundtrip_topology.atoms['atom_name'].tolist() == source_topology.atoms['atom_name'].tolist()


def test_parity_group_names(roundtrip_topology, source_topology):
    assert roundtrip_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()


def test_topology_self_conversion_applies_atom_subset(mda_topology):
    output = msm.convert(
        mda_topology,
        to_form='MDAnalysis.Topology',
        selection=[2, 0],
    )

    assert output.n_atoms == 2
    assert output.ids.values.tolist() == [3, 1]
