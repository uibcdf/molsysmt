"""
Tests for string_alphafold_id/get_topological_attributes.py.

Two-tier strategy
-----------------
1. Local tests (no network):
   Build a molsysmt.Topology from the bundled 1l2y.pdb and pass it directly
   to the string_alphafold_id getter functions with skip_digestion=True. This
   exercises the full delegation chain (string_alphafold_id → molsysmt_Topology)
   without any network download.

   Note: 1l2y.pdb is used here purely to exercise the getters; it is not
   an AlphaFold structure. The goal is to validate the delegation logic.

2. Network smoke test (@pytest.mark.network):
   A single test that verifies the AlphaFold download + conversion pipeline
   is alive, using AF-P62258-F1 (human 14-3-3 protein epsilon, 255 residues).
   Run with:  pytest -m network
   Skip with: pytest -m "not network"
"""

import pytest
from pathlib import Path

import molsysmt as msm
from molsysmt.form.string_alphafold_id import get_topological_attributes as aux

PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')

# Constants for the local 1l2y.pdb oracle (used to test delegation logic)
N_ATOMS       = 304
N_GROUPS      = 20
N_CHAINS      = 1
N_BONDS       = 310
N_MOLECULES   = 1
N_ENTITIES    = 1
N_COMPONENTS  = 1
N_AMINO_ACIDS = 20


@pytest.fixture(scope='module')
def topo():
    """molsysmt.Topology from the bundled 1l2y.pdb.

    Passed with skip_digestion=True to the string_alphafold_id getters so the
    delegation chain (string_alphafold_id → molsysmt_Topology) is exercised
    without a network download.
    """
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# System-level counts (local, no network)
# ---------------------------------------------------------------------------

def test_n_atoms(topo):
    assert aux.get_n_atoms_from_system(topo, skip_digestion=True) == N_ATOMS

def test_n_groups(topo):
    assert aux.get_n_groups_from_system(topo, skip_digestion=True) == N_GROUPS

def test_n_chains(topo):
    assert aux.get_n_chains_from_system(topo, skip_digestion=True) == N_CHAINS

def test_n_bonds(topo):
    assert aux.get_n_bonds_from_system(topo, skip_digestion=True) == N_BONDS

def test_n_molecules(topo):
    assert aux.get_n_molecules_from_system(topo, skip_digestion=True) == N_MOLECULES

def test_n_entities(topo):
    assert aux.get_n_entities_from_system(topo, skip_digestion=True) == N_ENTITIES

def test_n_components(topo):
    assert aux.get_n_components_from_system(topo, skip_digestion=True) == N_COMPONENTS

def test_n_amino_acids(topo):
    assert aux.get_n_amino_acids_from_system(topo, skip_digestion=True) == N_AMINO_ACIDS


# ---------------------------------------------------------------------------
# Group names (local)
# ---------------------------------------------------------------------------

def test_group_name_first_five(topo):
    names = aux.get_group_name_from_group(topo, skip_digestion=True)
    assert isinstance(names, list)
    assert len(names) == N_GROUPS
    assert names[:5] == ['ASN', 'LEU', 'TYR', 'ILE', 'GLN']

def test_group_name_last(topo):
    names = aux.get_group_name_from_group(topo, skip_digestion=True)
    assert names[-1] == 'SER'


# ---------------------------------------------------------------------------
# Chain identity (local)
# ---------------------------------------------------------------------------

def test_chain_id(topo):
    chain_ids = aux.get_chain_id_from_chain(topo, skip_digestion=True)
    assert isinstance(chain_ids, list)
    assert chain_ids == ['A']


# ---------------------------------------------------------------------------
# Atom-level consistency (local)
# ---------------------------------------------------------------------------

def test_atom_name_from_atom_length(topo):
    names = aux.get_atom_name_from_atom(topo, skip_digestion=True)
    assert isinstance(names, list)
    assert len(names) == N_ATOMS

def test_n_atoms_from_group_sums_to_total(topo):
    per_group = aux.get_n_atoms_from_group(topo, skip_digestion=True)
    assert isinstance(per_group, list)
    assert len(per_group) == N_GROUPS
    assert sum(per_group) == N_ATOMS

def test_bonded_atom_pairs_length(topo):
    pairs = aux.get_bonded_atom_pairs_from_system(topo, skip_digestion=True)
    assert isinstance(pairs, list)
    assert len(pairs) == N_BONDS


# ---------------------------------------------------------------------------
# Network smoke test — verify the AlphaFold download + conversion pipeline
# ---------------------------------------------------------------------------

@pytest.mark.network
def test_download_and_basic_count():
    """Download AF-P62258-F1 from AlphaFold and verify group count."""
    # Human 14-3-3 protein epsilon (YWHAE), 255 residues
    n = aux.get_n_groups_from_system('alphafold_id:AF-P62258-F1')
    assert n == 255
