"""
Parser regression tests for openmm.Modeller form adapter.

Uses a bundled PDB file (1l2y: Trp-cage miniprotein, 20 residues, 1 chain, 304 atoms)
to guard against regressions in the format-specific parsing logic. The Modeller is
built by converting the PDB to openmm.Modeller via msm.convert.

These tests are NOT exhaustive — they focus on the attributes most likely to be wrong
if the parser or converter has a bug: atom/group/chain counts, group names, chain IDs,
and bond counts.
"""

import pytest
from pathlib import Path

import molsysmt as msm
from molsysmt.form.openmm_Modeller import get_topological_attributes as aux

# Bundled PDB: Trp-cage miniprotein (1L2Y), 20 residues, 1 chain, 304 atoms
PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')

N_ATOMS      = 304
N_GROUPS     = 20
N_CHAINS     = 1
N_BONDS      = 310
N_MOLECULES  = 1
N_ENTITIES   = 1
N_COMPONENTS = 1
N_AMINO_ACIDS = 20


@pytest.fixture(scope='module')
def modeller():
    m = msm.convert(PDB_PATH, to_form='openmm.Modeller')
    assert m is not None
    return m


# ---------------------------------------------------------------------------
# System-level counts
# ---------------------------------------------------------------------------

def test_n_atoms(modeller):
    assert aux.get_n_atoms_from_system(modeller) == N_ATOMS

def test_n_groups(modeller):
    assert aux.get_n_groups_from_system(modeller) == N_GROUPS

def test_n_chains(modeller):
    assert aux.get_n_chains_from_system(modeller) == N_CHAINS

def test_n_bonds(modeller):
    assert aux.get_n_bonds_from_system(modeller) == N_BONDS

def test_n_molecules(modeller):
    assert aux.get_n_molecules_from_system(modeller) == N_MOLECULES

def test_n_entities(modeller):
    assert aux.get_n_entities_from_system(modeller) == N_ENTITIES

def test_n_components(modeller):
    assert aux.get_n_components_from_system(modeller) == N_COMPONENTS

def test_n_amino_acids(modeller):
    assert aux.get_n_amino_acids_from_system(modeller) == N_AMINO_ACIDS


# ---------------------------------------------------------------------------
# Group names and atom counts
# ---------------------------------------------------------------------------

def test_group_name_first_five(modeller):
    names = aux.get_group_name_from_group(modeller)
    assert isinstance(names, list)
    assert len(names) == N_GROUPS
    assert names[:5] == ['ASN', 'LEU', 'TYR', 'ILE', 'GLN']

def test_group_name_last(modeller):
    names = aux.get_group_name_from_group(modeller)
    assert names[-1] == 'SER'


# ---------------------------------------------------------------------------
# Chain identity
# ---------------------------------------------------------------------------

def test_chain_id(modeller):
    chain_ids = aux.get_chain_id_from_chain(modeller)
    assert isinstance(chain_ids, list)
    assert chain_ids == ['A']

def test_chain_name_is_none(modeller):
    assert aux.get_chain_name_from_chain(modeller) is None


# ---------------------------------------------------------------------------
# Atom indices length
# ---------------------------------------------------------------------------

def test_atom_index_from_group_length(modeller):
    result = aux.get_atom_index_from_group(modeller)
    assert isinstance(result, list)
    assert len(result) == N_GROUPS

def test_n_atoms_from_group_sums_to_total(modeller):
    per_group = aux.get_n_atoms_from_group(modeller)
    assert isinstance(per_group, list)
    assert len(per_group) == N_GROUPS
    assert sum(per_group) == N_ATOMS


# ---------------------------------------------------------------------------
# Bond sanity
# ---------------------------------------------------------------------------

def test_bonded_atom_pairs_length(modeller):
    pairs = aux.get_bonded_atom_pairs_from_system(modeller)
    assert isinstance(pairs, list)
    assert len(pairs) == N_BONDS
