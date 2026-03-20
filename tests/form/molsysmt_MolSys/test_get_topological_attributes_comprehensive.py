"""
Comprehensive tests for molsysmt_MolSys/get_topological_attributes.py using a
real PDB file (chicken villin HP35, 1vii.pdb).

This file covers all getters NOT already tested in
test_get_topological_attributes_from_pdb.py.

Notes on return semantics:
  - get_n_*_from_<source>  functions return a scalar int (total count), not a list.
  - get_bonded_atoms_from_bond returns np.unique of all bonded atom indices → len == N_ATOMS.
  - get_bonded_atom_pairs_from_atom / get_inner_bonded_atom_pairs_from_atom
    return one entry per bond → len == N_BONDS.
  - get_inner_bonded_atoms_from_system / get_bonded_atoms_from_system
    delegate to get_bonded_atoms_from_bond → len == N_ATOMS.
"""

import pytest
from molsysmt.form.molsysmt_MolSys import get_topological_attributes as aux

N_ATOMS      = 596
N_GROUPS     = 36
N_COMPONENTS = 1
N_MOLECULES  = 1
N_ENTITIES   = 1
N_CHAINS     = 1
N_BONDS      = 602


# ---------------------------------------------------------------------------
# Atom level — list functions (return list of length N_ATOMS)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_component_id_from_atom",
    "get_component_name_from_atom",
    "get_component_type_from_atom",
    "get_chain_type_from_atom",
    "get_bond_type_from_atom",
    "get_bond_order_from_atom",
    "get_inner_bonded_atoms_from_atom",
])
def test_atom_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_ATOMS


# Atom level — bond-pair functions: indexed by bond, not atom
@pytest.mark.parametrize("func_name", [
    "get_bonded_atom_pairs_from_atom",
    "get_inner_bonded_atom_pairs_from_atom",
])
def test_atom_bond_pair_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_BONDS


# Atom level — scalar count functions (return int, not list)
@pytest.mark.parametrize("func_name", [
    "get_n_components_from_atom",
    "get_n_molecules_from_atom",
    "get_n_chains_from_atom",
    "get_n_entities_from_atom",
    "get_n_inner_bonds_from_atom",
    "get_n_amino_acids_from_atom",
    "get_n_nucleotides_from_atom",
    "get_n_ions_from_atom",
    "get_n_waters_from_atom",
    "get_n_small_molecules_from_atom",
    "get_n_peptides_from_atom",
    "get_n_proteins_from_atom",
    "get_n_dnas_from_atom",
    "get_n_rnas_from_atom",
    "get_n_lipids_from_atom",
    "get_n_polysaccharides_from_atom",
    "get_n_saccharides_from_atom",
])
def test_atom_scalar_not_none(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None


# ---------------------------------------------------------------------------
# Group level — list functions (return list of length N_GROUPS)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_id_from_group",
    "get_atom_type_from_group",
    "get_component_index_from_group",
    "get_component_id_from_group",
    "get_component_name_from_group",
    "get_component_type_from_group",
    "get_molecule_id_from_group",
    "get_molecule_name_from_group",
    "get_molecule_type_from_group",
    "get_entity_index_from_group",
    "get_entity_id_from_group",
    "get_entity_name_from_group",
    "get_entity_type_from_group",
    "get_chain_id_from_group",
    "get_chain_name_from_group",
    "get_chain_type_from_group",
])
def test_group_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_GROUPS


# Group level — scalar count functions
@pytest.mark.parametrize("func_name", [
    "get_n_groups_from_group",
    "get_n_components_from_group",
    "get_n_molecules_from_group",
    "get_n_entities_from_group",
    "get_n_chains_from_group",
])
def test_group_scalar_not_none(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None


# ---------------------------------------------------------------------------
# Component level — list functions (return list of length N_COMPONENTS)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_id_from_component",
    "get_atom_name_from_component",
    "get_atom_type_from_component",
    "get_group_index_from_component",
    "get_group_id_from_component",
    "get_group_name_from_component",
    "get_group_type_from_component",
    "get_component_index_from_component",
    "get_component_id_from_component",
    "get_component_name_from_component",
    "get_component_type_from_component",
    "get_molecule_index_from_component",
    "get_molecule_id_from_component",
    "get_molecule_name_from_component",
    "get_molecule_type_from_component",
    "get_entity_index_from_component",
    "get_entity_id_from_component",
    "get_entity_name_from_component",
    "get_entity_type_from_component",
    "get_chain_index_from_component",
    "get_chain_id_from_component",
    "get_chain_name_from_component",
    "get_chain_type_from_component",
])
def test_component_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_COMPONENTS


# Component level — scalar count functions
@pytest.mark.parametrize("func_name", [
    "get_n_atoms_from_component",
    "get_n_groups_from_component",
    "get_n_components_from_component",
    "get_n_molecules_from_component",
    "get_n_chains_from_component",
    "get_n_entities_from_component",
    "get_n_bonds_from_component",
    "get_n_inner_bonds_from_component",
    "get_n_amino_acids_from_component",
    "get_n_nucleotides_from_component",
    "get_n_ions_from_component",
    "get_n_waters_from_component",
    "get_n_small_molecules_from_component",
    "get_n_peptides_from_component",
    "get_n_proteins_from_component",
    "get_n_dnas_from_component",
    "get_n_rnas_from_component",
    "get_n_lipids_from_component",
    "get_n_polysaccharides_from_component",
    "get_n_saccharides_from_component",
])
def test_component_scalar_not_none(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None


# ---------------------------------------------------------------------------
# Molecule level — list functions (return list of length N_MOLECULES)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_id_from_molecule",
    "get_atom_name_from_molecule",
    "get_atom_type_from_molecule",
    "get_group_index_from_molecule",
    "get_group_id_from_molecule",
    "get_group_name_from_molecule",
    "get_group_type_from_molecule",
    "get_component_index_from_molecule",
    "get_component_id_from_molecule",
    "get_component_name_from_molecule",
    "get_component_type_from_molecule",
    "get_molecule_index_from_molecule",
    "get_molecule_id_from_molecule",
    "get_molecule_name_from_molecule",
    "get_entity_index_from_molecule",
    "get_entity_id_from_molecule",
    "get_entity_name_from_molecule",
    "get_entity_type_from_molecule",
    "get_chain_index_from_molecule",
    "get_chain_id_from_molecule",
    "get_chain_name_from_molecule",
    "get_chain_type_from_molecule",
])
def test_molecule_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_MOLECULES


# Molecule level — scalar count functions
@pytest.mark.parametrize("func_name", [
    "get_n_atoms_from_molecule",
    "get_n_groups_from_molecule",
    "get_n_components_from_molecule",
    "get_n_molecules_from_molecule",
    "get_n_chains_from_molecule",
    "get_n_entities_from_molecule",
    "get_n_bonds_from_molecule",
    "get_n_inner_bonds_from_molecule",
    "get_n_amino_acids_from_molecule",
    "get_n_nucleotides_from_molecule",
    "get_n_ions_from_molecule",
    "get_n_waters_from_molecule",
    "get_n_small_molecules_from_molecule",
    "get_n_peptides_from_molecule",
    "get_n_proteins_from_molecule",
    "get_n_dnas_from_molecule",
    "get_n_rnas_from_molecule",
    "get_n_lipids_from_molecule",
    "get_n_polysaccharides_from_molecule",
    "get_n_saccharides_from_molecule",
])
def test_molecule_scalar_not_none(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None


# ---------------------------------------------------------------------------
# Entity level — list functions (return list of length N_ENTITIES)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_id_from_entity",
    "get_atom_name_from_entity",
    "get_atom_type_from_entity",
    "get_group_index_from_entity",
    "get_group_id_from_entity",
    "get_group_name_from_entity",
    "get_group_type_from_entity",
    "get_component_index_from_entity",
    "get_component_id_from_entity",
    "get_component_name_from_entity",
    "get_component_type_from_entity",
    "get_molecule_index_from_entity",
    "get_molecule_id_from_entity",
    "get_molecule_name_from_entity",
    "get_molecule_type_from_entity",
    "get_entity_index_from_entity",
    "get_entity_id_from_entity",
    "get_entity_name_from_entity",
    "get_entity_type_from_entity",
    "get_chain_index_from_entity",
    "get_chain_id_from_entity",
    "get_chain_name_from_entity",
    "get_chain_type_from_entity",
])
def test_entity_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_ENTITIES


# Entity level — scalar count functions
@pytest.mark.parametrize("func_name", [
    "get_n_atoms_from_entity",
    "get_n_groups_from_entity",
    "get_n_components_from_entity",
    "get_n_molecules_from_entity",
    "get_n_chains_from_entity",
    "get_n_entities_from_entity",
    "get_n_bonds_from_entity",
    "get_n_inner_bonds_from_entity",
    "get_n_amino_acids_from_entity",
    "get_n_nucleotides_from_entity",
    "get_n_ions_from_entity",
    "get_n_waters_from_entity",
    "get_n_small_molecules_from_entity",
    "get_n_peptides_from_entity",
    "get_n_proteins_from_entity",
    "get_n_dnas_from_entity",
    "get_n_rnas_from_entity",
    "get_n_lipids_from_entity",
    "get_n_polysaccharides_from_entity",
    "get_n_saccharides_from_entity",
])
def test_entity_scalar_not_none(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None


# ---------------------------------------------------------------------------
# Chain level — list functions (return list of length N_CHAINS)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_id_from_chain",
    "get_atom_name_from_chain",
    "get_atom_type_from_chain",
    "get_group_index_from_chain",
    "get_group_id_from_chain",
    "get_group_name_from_chain",
    "get_group_type_from_chain",
    "get_component_index_from_chain",
    "get_component_id_from_chain",
    "get_component_name_from_chain",
    "get_component_type_from_chain",
    "get_molecule_index_from_chain",
    "get_molecule_id_from_chain",
    "get_molecule_name_from_chain",
    "get_molecule_type_from_chain",
    "get_entity_index_from_chain",
    "get_entity_id_from_chain",
    "get_entity_name_from_chain",
    "get_entity_type_from_chain",
    "get_chain_index_from_chain",
    "get_chain_name_from_chain",
    "get_chain_type_from_chain",
])
def test_chain_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_CHAINS


# Chain level — scalar count functions
@pytest.mark.parametrize("func_name", [
    "get_n_atoms_from_chain",
    "get_n_groups_from_chain",
    "get_n_components_from_chain",
    "get_n_molecules_from_chain",
    "get_n_chains_from_chain",
    "get_n_entities_from_chain",
    "get_n_bonds_from_chain",
    "get_n_inner_bonds_from_chain",
    "get_n_amino_acids_from_chain",
    "get_n_nucleotides_from_chain",
    "get_n_ions_from_chain",
    "get_n_waters_from_chain",
    "get_n_small_molecules_from_chain",
    "get_n_peptides_from_chain",
    "get_n_proteins_from_chain",
    "get_n_dnas_from_chain",
    "get_n_rnas_from_chain",
    "get_n_lipids_from_chain",
    "get_n_polysaccharides_from_chain",
    "get_n_saccharides_from_chain",
])
def test_chain_scalar_not_none(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None


# ---------------------------------------------------------------------------
# Bond level — list functions (return list of length N_BONDS)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_bond_index_from_bond",
    "get_bond_order_from_bond",
    "get_bond_type_from_bond",
    "get_bonded_atom_pairs_from_bond",
])
def test_bond_array_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_BONDS


def test_get_bonded_atoms_from_bond_length(hp35_pdb_molsys):
    """get_bonded_atoms_from_bond returns unique bonded atoms (len == N_ATOMS)."""
    result = aux.get_bonded_atoms_from_bond(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_ATOMS


def test_get_n_bonds_from_bond_scalar(hp35_pdb_molsys):
    """get_n_bonds_from_bond with indices='all' returns total bond count (scalar)."""
    result = aux.get_n_bonds_from_bond(hp35_pdb_molsys)
    assert result is not None
    assert result == N_BONDS


# ---------------------------------------------------------------------------
# System level — remaining count functions (return int)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, expected", [
    ("get_n_small_molecules_from_system",  0),
    ("get_n_proteins_from_system",         0),  # HP35 (36 residues) is peptide, not protein
    ("get_n_dnas_from_system",             0),
    ("get_n_rnas_from_system",             0),
    ("get_n_lipids_from_system",           0),
    ("get_n_polysaccharides_from_system",  0),
    ("get_n_saccharides_from_system",      0),
])
def test_system_count(hp35_pdb_molsys, func_name, expected):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, int)
    assert result == expected


# ---------------------------------------------------------------------------
# System level — bonded atoms functions
# get_inner_bonded_atoms_from_system and get_bonded_atoms_from_system both
# delegate to get_bonded_atoms_from_bond, which returns unique atom indices
# → length == N_ATOMS (not N_BONDS).
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_inner_bonded_atoms_from_system",
    "get_bonded_atoms_from_system",
])
def test_system_bonded_atoms_length(hp35_pdb_molsys, func_name):
    result = getattr(aux, func_name)(hp35_pdb_molsys)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == N_ATOMS
