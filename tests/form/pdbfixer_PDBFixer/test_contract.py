"""
Contract and parity tests for pdbfixer.PDBFixer form.

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, all hydrogens present).
Because 1l2y already has all hydrogens and no missing residues,
pdbfixer introduces no changes — atom count is preserved.

Contract: PDBFixer can be created and converted to molsysmt.Topology.
Parity: PDBFixer topology == source PDB topology (same counts, same names).
"""

import pytest
from pathlib import Path
import molsysmt as msm


PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')
N_ATOMS  = 304
N_GROUPS = 20
N_CHAINS = 1


@pytest.fixture(scope='module')
def fixer():
    from pdbfixer import PDBFixer
    return PDBFixer(PDB_PATH)


@pytest.fixture(scope='module')
def fixer_topology(fixer):
    return msm.convert(fixer, to_form='molsysmt.Topology')


@pytest.fixture(scope='module')
def source_topology():
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: PDBFixer can be created and converted to molsysmt.Topology
# ---------------------------------------------------------------------------

def test_fixer_is_created(fixer):
    from pdbfixer import PDBFixer
    assert isinstance(fixer, PDBFixer)


def test_fixer_topology_atom_count(fixer_topology):
    assert fixer_topology.n_atoms == N_ATOMS


def test_fixer_topology_group_count(fixer_topology):
    assert fixer_topology.n_groups == N_GROUPS


def test_fixer_topology_chain_count(fixer_topology):
    assert fixer_topology.n_chains == N_CHAINS


# ---------------------------------------------------------------------------
# Parity: PDBFixer topology == source PDB topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(fixer_topology, source_topology):
    assert fixer_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(fixer_topology, source_topology):
    assert fixer_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(fixer_topology, source_topology):
    assert fixer_topology.n_chains == source_topology.n_chains


def test_parity_group_names(fixer_topology, source_topology):
    assert fixer_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()

# Note: atom names are intentionally not compared here.  PDBFixer normalises
# hydrogen names to OpenMM conventions (e.g. H1 → H), so atom-name parity
# with the raw PDB parser is not expected.
