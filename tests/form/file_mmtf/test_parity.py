"""
Contract and parity tests for file:mmtf form.

file:mmtf is a binary compressed structure format (MMTF = Macromolecular
Transmission Format).  It is read via the mmtf library.

Oracle: 1l2y.mmtf (Trp-cage, 304 atoms, 20 residues, 1 chain, 38 NMR
models stored as multi-frame trajectory).  The file lives in
molsysmt/data/mmtf/ and requires no network access.

Parity oracle: 1l2y.pdb — same structure in PDB format.  Atom names and
group names must match between the MMTF and PDB parsers.

Note: the MMTF multi-model file returns only the first model (304 atoms)
when converting to molsysmt.Topology.
"""

import pytest
from pathlib import Path
import molsysmt as msm


MMTF_PATH = str(Path(msm.__file__).parent / 'data' / 'mmtf' / '1l2y.mmtf')
PDB_PATH  = str(Path(msm.__file__).parent / 'data' / 'pdb'  / '1l2y.pdb')
N_ATOMS   = 304
N_GROUPS  = 20
N_CHAINS  = 1


@pytest.fixture(scope='module')
def mmtf_topology():
    return msm.convert(MMTF_PATH, to_form='molsysmt.Topology')


@pytest.fixture(scope='module')
def source_topology():
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: file:mmtf can be read and converted to molsysmt.Topology
# ---------------------------------------------------------------------------

def test_mmtf_file_exists():
    import os
    assert os.path.isfile(MMTF_PATH)


def test_mmtf_is_form():
    from molsysmt.form.file_mmtf import is_form
    assert is_form(MMTF_PATH)


def test_mmtf_topology_atom_count(mmtf_topology):
    assert mmtf_topology.n_atoms == N_ATOMS


def test_mmtf_topology_group_count(mmtf_topology):
    assert mmtf_topology.n_groups == N_GROUPS


def test_mmtf_topology_chain_count(mmtf_topology):
    assert mmtf_topology.n_chains == N_CHAINS


# ---------------------------------------------------------------------------
# Parity: file:mmtf topology == file:pdb topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(mmtf_topology, source_topology):
    assert mmtf_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(mmtf_topology, source_topology):
    assert mmtf_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(mmtf_topology, source_topology):
    assert mmtf_topology.n_chains == source_topology.n_chains


def test_parity_atom_names(mmtf_topology, source_topology):
    assert mmtf_topology.atoms['atom_name'].tolist() == source_topology.atoms['atom_name'].tolist()


def test_parity_group_names(mmtf_topology, source_topology):
    assert mmtf_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()
