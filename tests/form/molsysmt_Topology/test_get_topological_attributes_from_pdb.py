"""
Tests for molsysmt_Topology/get_topological_attributes.py using a real PDB file
(chicken villin HP35, 1vii.pdb). This fixture exercises the PDB parser and the
MolSys → molsysmt.Topology conversion pipeline.

Expected values were verified by running the functions against the parsed structure.
"""

import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux

N_ATOMS      = 596
N_GROUPS     = 36
N_CHAINS     = 1
N_MOLECULES  = 1
N_ENTITIES   = 1
N_COMPONENTS = 1
N_BONDS      = 602


@pytest.fixture(scope="module")
def topo():
    molsys = msm.convert(msm.systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys')
    return msm.convert(molsys, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# System-level counts — validate parser correctness
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, expected", [
    ("get_n_atoms_from_system",       N_ATOMS),
    ("get_n_groups_from_system",      N_GROUPS),
    ("get_n_components_from_system",  N_COMPONENTS),
    ("get_n_molecules_from_system",   N_MOLECULES),
    ("get_n_entities_from_system",    N_ENTITIES),
    ("get_n_chains_from_system",      N_CHAINS),
    ("get_n_bonds_from_system",       N_BONDS),
    ("get_n_amino_acids_from_system", 36),
    ("get_n_nucleotides_from_system", 0),
    ("get_n_ions_from_system",        0),
    ("get_n_waters_from_system",      0),
    ("get_n_peptides_from_system",    1),
    ("get_n_proteins_from_system",    0),
    ("get_n_dnas_from_system",        0),
    ("get_n_rnas_from_system",        0),
])
def test_system_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


@pytest.mark.parametrize("func_name", [
    "get_bond_index_from_system",
    "get_bonded_atom_pairs_from_system",
    "get_inner_bonded_atom_pairs_from_system",
])
def test_system_bond_pairs_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDS


# ---------------------------------------------------------------------------
# Atom-level array lengths
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_atom",
    "get_atom_id_from_atom",
    "get_atom_name_from_atom",
    "get_atom_type_from_atom",
    "get_group_index_from_atom",
    "get_group_id_from_atom",
    "get_group_name_from_atom",
    "get_group_type_from_atom",
    "get_molecule_index_from_atom",
    "get_molecule_id_from_atom",
    "get_molecule_name_from_atom",
    "get_molecule_type_from_atom",
    "get_entity_index_from_atom",
    "get_entity_id_from_atom",
    "get_entity_name_from_atom",
    "get_entity_type_from_atom",
    "get_component_index_from_atom",
    "get_chain_index_from_atom",
    "get_chain_id_from_atom",
    "get_chain_name_from_atom",
    "get_bond_index_from_atom",
    "get_bonded_atoms_from_atom",
    "get_inner_bond_index_from_atom",
    "get_n_bonds_from_atom",
])
def test_atom_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_ATOMS


# ---------------------------------------------------------------------------
# Group-level array lengths
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_group",
    "get_atom_name_from_group",
    "get_group_index_from_group",
    "get_group_id_from_group",
    "get_group_name_from_group",
    "get_group_type_from_group",
    "get_molecule_index_from_group",
    "get_chain_index_from_group",
    "get_n_atoms_from_group",
    "get_n_bonds_from_group",
])
def test_group_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_GROUPS


# ---------------------------------------------------------------------------
# Spot checks — verify parser correctness for specific values
# ---------------------------------------------------------------------------

def test_first_atom_name(topo):
    names = aux.get_atom_name_from_atom(topo)
    assert names[0] == 'N'


def test_first_group_name(topo):
    names = aux.get_group_name_from_group(topo)
    assert names[0] == 'MET'


def test_chain_id(topo):
    ids = aux.get_chain_id_from_chain(topo)
    assert ids == ['A']


def test_molecule_type(topo):
    types = aux.get_molecule_type_from_molecule(topo)
    assert types == ['peptide']


def test_n_amino_acids_equals_n_groups(topo):
    assert aux.get_n_amino_acids_from_system(topo) == aux.get_n_groups_from_system(topo)


def test_total_bond_count_from_atom(topo):
    assert aux.get_total_n_bonds_from_atom(topo) == N_BONDS


def test_n_atoms_from_atom(topo):
    assert aux.get_n_atoms_from_atom(topo) == N_ATOMS


def test_n_groups_from_atom(topo):
    assert aux.get_n_groups_from_atom(topo) == N_GROUPS
