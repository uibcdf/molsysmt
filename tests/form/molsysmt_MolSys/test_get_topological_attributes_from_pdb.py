"""
Tests for molsysmt_MolSys/get_topological_attributes.py using a real PDB file
(chicken villin HP35, 1vii.pdb).

All getters delegate to molsysmt_Topology; these tests ensure the MolSys wrapper
layer is exercised and that the delegation is transparent to the caller.

Expected values match test_get_topological_attributes_from_pdb.py in
tests/form/molsysmt_Topology/ (same structure, different form).
"""

import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_MolSys import get_topological_attributes as aux

N_ATOMS      = 596
N_GROUPS     = 36
N_CHAINS     = 1
N_MOLECULES  = 1
N_ENTITIES   = 1
N_COMPONENTS = 1
N_BONDS      = 602


# ---------------------------------------------------------------------------
# System-level counts
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
])
def test_system_count(hp35_pdb_molsys, func_name, expected):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result == expected


@pytest.mark.parametrize("func_name", [
    "get_bond_index_from_system",
    "get_bonded_atom_pairs_from_system",
    "get_inner_bonded_atom_pairs_from_system",
])
def test_system_bond_pairs_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
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
def test_atom_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
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
])
def test_group_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert isinstance(result, list)
    assert len(result) == N_GROUPS


# ---------------------------------------------------------------------------
# Component, molecule, entity, chain — array lengths
# ---------------------------------------------------------------------------

def test_component_array_length(hp35_pdb_molsys):
    result = aux.get_atom_index_from_component(hp35_pdb_molsys)
    assert isinstance(result, list)
    assert len(result) == N_COMPONENTS


def test_molecule_array_length(hp35_pdb_molsys):
    result = aux.get_atom_index_from_molecule(hp35_pdb_molsys)
    assert isinstance(result, list)
    assert len(result) == N_MOLECULES


def test_entity_array_length(hp35_pdb_molsys):
    result = aux.get_atom_index_from_entity(hp35_pdb_molsys)
    assert isinstance(result, list)
    assert len(result) == N_ENTITIES


def test_chain_array_length(hp35_pdb_molsys):
    result = aux.get_atom_index_from_chain(hp35_pdb_molsys)
    assert isinstance(result, list)
    assert len(result) == N_CHAINS


# ---------------------------------------------------------------------------
# Spot checks
# ---------------------------------------------------------------------------

def test_first_atom_name(hp35_pdb_molsys):
    names = aux.get_atom_name_from_atom(hp35_pdb_molsys)
    assert names[0] == 'N'


def test_first_group_name(hp35_pdb_molsys):
    names = aux.get_group_name_from_group(hp35_pdb_molsys)
    assert names[0] == 'MET'


def test_chain_id(hp35_pdb_molsys):
    ids = aux.get_chain_id_from_chain(hp35_pdb_molsys)
    assert ids == ['A']


def test_molecule_type(hp35_pdb_molsys):
    types = aux.get_molecule_type_from_molecule(hp35_pdb_molsys)
    assert types == ['peptide']


def test_n_amino_acids_equals_n_groups(hp35_pdb_molsys):
    assert aux.get_n_amino_acids_from_system(hp35_pdb_molsys) == N_GROUPS


def test_n_atoms_from_atom(hp35_pdb_molsys):
    assert aux.get_n_atoms_from_atom(hp35_pdb_molsys) == N_ATOMS


def test_n_groups_from_atom(hp35_pdb_molsys):
    assert aux.get_n_groups_from_atom(hp35_pdb_molsys) == N_GROUPS


def test_form(hp35_pdb_molsys):
    result = msm.get_form(hp35_pdb_molsys)
    assert result == 'molsysmt.MolSys'
