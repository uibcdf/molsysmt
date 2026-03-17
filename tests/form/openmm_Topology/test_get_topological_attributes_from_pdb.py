"""
Parser regression tests for openmm.Topology form adapter.

Uses a bundled PDB file (1l2y: Trp-cage miniprotein, 20 residues, 1 chain, 304 atoms)
to guard against regressions in the format-specific parsing logic of the adapter.

These tests are NOT exhaustive — they focus on the attributes most likely to
be wrong if the parser or converter has a bug: atom/group/chain counts, group
names, chain IDs, and bond counts.
"""

import pytest
from pathlib import Path

import molsysmt as msm
from molsysmt.form.openmm_Topology import get_topological_attributes as aux

# Bundled PDB: Trp-cage miniprotein (1L2Y), 20 residues, 1 chain, 304 atoms
PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')

N_ATOMS    = 304
N_GROUPS   = 20
N_CHAINS   = 1
N_BONDS    = 310
N_MOLECULES = 1
N_ENTITIES  = 1
N_COMPONENTS = 1
N_AMINO_ACIDS = 20


@pytest.fixture(scope='module')
def topo():
    t = msm.convert(PDB_PATH, to_form='openmm.Topology')
    assert t is not None
    return t


# ---------------------------------------------------------------------------
# System-level counts
# ---------------------------------------------------------------------------

def test_n_atoms(topo):
    assert aux.get_n_atoms_from_system(topo) == N_ATOMS

def test_n_groups(topo):
    assert aux.get_n_groups_from_system(topo) == N_GROUPS

def test_n_chains(topo):
    assert aux.get_n_chains_from_system(topo) == N_CHAINS

def test_n_bonds(topo):
    assert aux.get_n_bonds_from_system(topo) == N_BONDS

def test_n_molecules(topo):
    assert aux.get_n_molecules_from_system(topo) == N_MOLECULES

def test_n_entities(topo):
    assert aux.get_n_entities_from_system(topo) == N_ENTITIES

def test_n_components(topo):
    assert aux.get_n_components_from_system(topo) == N_COMPONENTS

def test_n_amino_acids(topo):
    assert aux.get_n_amino_acids_from_system(topo) == N_AMINO_ACIDS


# ---------------------------------------------------------------------------
# Group names and atom counts
# ---------------------------------------------------------------------------

def test_group_name_first_five(topo):
    names = aux.get_group_name_from_group(topo)
    assert isinstance(names, list)
    assert len(names) == N_GROUPS
    # 1L2Y sequence: ASN-LEU-TYR-ILE-GLN-...
    assert names[:5] == ['ASN', 'LEU', 'TYR', 'ILE', 'GLN']

def test_group_name_last(topo):
    names = aux.get_group_name_from_group(topo)
    assert names[-1] == 'SER'


# ---------------------------------------------------------------------------
# Chain identity
# ---------------------------------------------------------------------------

def test_chain_id(topo):
    chain_ids = aux.get_chain_id_from_chain(topo)
    assert isinstance(chain_ids, list)
    assert chain_ids == ['A']

def test_chain_name_is_none(topo):
    assert aux.get_chain_name_from_chain(topo) is None


# ---------------------------------------------------------------------------
# Atom indices length
# ---------------------------------------------------------------------------

def test_atom_index_from_group_length(topo):
    result = aux.get_atom_index_from_group(topo)
    assert isinstance(result, list)
    assert len(result) == N_GROUPS

def test_n_atoms_from_group_sums_to_total(topo):
    per_group = aux.get_n_atoms_from_group(topo)
    assert isinstance(per_group, list)
    assert len(per_group) == N_GROUPS
    assert sum(per_group) == N_ATOMS


# ---------------------------------------------------------------------------
# Bond sanity
# ---------------------------------------------------------------------------

def test_bonded_atom_pairs_length(topo):
    pairs = aux.get_bonded_atom_pairs_from_system(topo)
    assert isinstance(pairs, list)
    assert len(pairs) == N_BONDS
