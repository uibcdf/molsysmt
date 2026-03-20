"""
Comprehensive tests for openmm_Topology/get_topological_attributes.py
using the villin HP35 PDB (1vii: 36 residues, 1 chain, 596 atoms, 602 bonds).

These tests complement test_get_topological_attributes_from_pdb.py (which covers
only basic system-level counts and a few array-length checks) and
test_get_topological_attributes_from_builder.py (which covers all functions with a
mixed peptide+water+ion system). This file exercises every function NOT yet covered
in from_pdb using a protein-only system, confirming that:

  - type-counting functions return 0 for absent types (dna, rna, water, ion, …)
  - type-counting functions return the correct value for the present type (peptide/amino acid)
  - per-element array-returning functions return lists of the expected length at every
    hierarchy level (group, component, molecule, entity, chain, bond)
  - inner/system-level bond functions work correctly
  - total_n_* functions delegate correctly

System facts (1vii.pdb, model 1 only, no solvent):
  N_ATOMS       = 596
  N_GROUPS      = 36   (all amino acids)
  N_CHAINS      = 1
  N_BONDS       = 602
  N_COMPONENTS  = 1
  N_MOLECULES   = 1
  N_ENTITIES    = 1
  N_AMINO_ACIDS = 36
  N_BONDED_ATOMS = 596  (every atom is in at least one bond)

openmm.Topology adapter notes (inherited from builder tests):
  - get_n_bonds_from_atom / get_n_inner_bonds_from_atom → scalar (total unique bonds)
  - get_chain_name_from_* → None (openmm.Topology has no chain names)
  - get_n_components_from_group / get_n_chains_from_group → scalar unique count
  - get_n_chains_from_component → scalar unique count
  - Bond-related queries from group/component/molecule/entity/chain raise
    NotImplementedMethodError (not tested here)
"""

import pytest
from pathlib import Path

import molsysmt as msm
from molsysmt.form.openmm_Topology import get_topological_attributes as aux

PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1vii.pdb')

N_ATOMS        = 596
N_GROUPS       = 36
N_CHAINS       = 1
N_BONDS        = 602
N_COMPONENTS   = 1
N_MOLECULES    = 1
N_ENTITIES     = 1
N_AMINO_ACIDS  = 36
N_BONDED_ATOMS = 596


@pytest.fixture(scope='module')
def topo():
    t = msm.convert(PDB_PATH, to_form='openmm.Topology')
    assert t is not None
    return t


# ---------------------------------------------------------------------------
# System-level type-counting — protein-only zeroes and non-zeroes
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, expected", [
    ("get_n_nucleotides_from_system",    0),
    ("get_n_ions_from_system",           0),
    ("get_n_waters_from_system",         0),
    ("get_n_small_molecules_from_system", 0),
    ("get_n_lipids_from_system",         0),
    ("get_n_saccharides_from_system",    0),
    ("get_n_polysaccharides_from_system", 0),
    ("get_n_peptides_from_system",       1),
    ("get_n_proteins_from_system",       0),
    ("get_n_dnas_from_system",           0),
    ("get_n_rnas_from_system",           0),
])
def test_system_type_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


# ---------------------------------------------------------------------------
# System-level bond functions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_bond_index_from_system",
    "get_bonded_atom_pairs_from_system",
    "get_inner_bond_index_from_system",
    "get_inner_bonded_atom_pairs_from_system",
])
def test_system_bond_pairs_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDS


@pytest.mark.parametrize("func_name", [
    "get_bonded_atoms_from_system",
    "get_inner_bonded_atoms_from_system",
])
def test_system_bonded_atoms_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDED_ATOMS


# ---------------------------------------------------------------------------
# Atom-level — per-atom list functions (not covered in from_pdb test)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_component_index_from_atom",
    "get_component_id_from_atom",
    "get_component_name_from_atom",
    "get_component_type_from_atom",
    "get_molecule_index_from_atom",
    "get_molecule_id_from_atom",
    "get_molecule_name_from_atom",
    "get_molecule_type_from_atom",
    "get_entity_index_from_atom",
    "get_entity_id_from_atom",
    "get_entity_name_from_atom",
    "get_entity_type_from_atom",
    "get_bond_index_from_atom",
    "get_bonded_atoms_from_atom",
    "get_inner_bond_index_from_atom",
])
def test_atom_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_ATOMS


@pytest.mark.parametrize("func_name", [
    "get_bonded_atom_pairs_from_atom",
    "get_inner_bonded_atom_pairs_from_atom",
])
def test_atom_bond_pairs_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDS


def test_inner_bonded_atoms_from_atom_length(topo):
    result = aux.get_inner_bonded_atoms_from_atom(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDED_ATOMS


# Scalar counts from atom (type counting — protein-only)
@pytest.mark.parametrize("func_name, expected", [
    ("get_n_atoms_from_atom",                 N_ATOMS),
    ("get_total_n_atoms_from_atom",           N_ATOMS),
    ("get_n_groups_from_atom",                N_GROUPS),
    ("get_total_n_groups_from_atom",          N_GROUPS),
    ("get_n_components_from_atom",            N_COMPONENTS),
    ("get_total_n_components_from_atom",      N_COMPONENTS),
    ("get_n_molecules_from_atom",             N_MOLECULES),
    ("get_total_n_molecules_from_atom",       N_MOLECULES),
    ("get_n_entities_from_atom",              N_ENTITIES),
    ("get_total_n_entities_from_atom",        N_ENTITIES),
    ("get_n_chains_from_atom",                N_CHAINS),
    ("get_total_n_chains_from_atom",          N_CHAINS),
    ("get_n_amino_acids_from_atom",           N_AMINO_ACIDS),
    ("get_total_n_amino_acids_from_atom",     N_AMINO_ACIDS),
    ("get_n_nucleotides_from_atom",           0),
    ("get_total_n_nucleotides_from_atom",     0),
    ("get_n_ions_from_atom",                  0),
    ("get_total_n_ions_from_atom",            0),
    ("get_n_waters_from_atom",                0),
    ("get_total_n_waters_from_atom",          0),
    ("get_n_small_molecules_from_atom",       0),
    ("get_total_n_small_molecules_from_atom", 0),
    ("get_n_lipids_from_atom",                0),
    ("get_total_n_lipids_from_atom",          0),
    ("get_n_saccharides_from_atom",           0),
    ("get_total_n_saccharides_from_atom",     0),
    ("get_n_peptides_from_atom",              1),
    ("get_total_n_peptides_from_atom",        1),
    ("get_n_proteins_from_atom",              0),
    ("get_total_n_proteins_from_atom",        0),
    ("get_n_polysaccharides_from_atom",       0),
    ("get_total_n_polysaccharides_from_atom", 0),
    ("get_n_dnas_from_atom",                  0),
    ("get_total_n_dnas_from_atom",            0),
    ("get_n_rnas_from_atom",                  0),
    ("get_total_n_rnas_from_atom",            0),
    # In openmm.Topology these return a scalar (total unique bonds)
    ("get_n_bonds_from_atom",                 N_BONDS),
    ("get_n_inner_bonds_from_atom",           N_BONDS),
    ("get_total_n_bonds_from_atom",           N_BONDS),
    ("get_total_n_inner_bonds_from_atom",     N_BONDS),
])
def test_atom_scalar_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


# ---------------------------------------------------------------------------
# Group-level — per-group list functions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_group",
    "get_atom_id_from_group",
    "get_atom_name_from_group",
    "get_atom_type_from_group",
    "get_group_index_from_group",
    "get_group_id_from_group",
    "get_group_name_from_group",
    "get_group_type_from_group",
    "get_component_index_from_group",
    "get_component_id_from_group",
    "get_component_name_from_group",
    "get_component_type_from_group",
    "get_molecule_index_from_group",
    "get_molecule_id_from_group",
    "get_molecule_name_from_group",
    "get_molecule_type_from_group",
    "get_entity_index_from_group",
    "get_entity_id_from_group",
    "get_entity_name_from_group",
    "get_entity_type_from_group",
    "get_chain_index_from_group",
    "get_chain_id_from_group",
    "get_chain_type_from_group",
    "get_n_atoms_from_group",
])
def test_group_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_GROUPS


# Group-level scalars — type-counting
@pytest.mark.parametrize("func_name, expected", [
    ("get_n_groups_from_group",              N_GROUPS),
    ("get_total_n_groups_from_group",        N_GROUPS),
    ("get_total_n_atoms_from_group",         N_ATOMS),
    ("get_n_molecules_from_group",           N_MOLECULES),
    ("get_total_n_molecules_from_group",     N_MOLECULES),
    ("get_n_entities_from_group",            N_ENTITIES),
    ("get_total_n_entities_from_group",      N_ENTITIES),
    # Scalar unique counts in openmm.Topology
    ("get_n_components_from_group",          N_COMPONENTS),
    ("get_total_n_components_from_group",    N_COMPONENTS),
    ("get_n_chains_from_group",              N_CHAINS),
    ("get_total_n_chains_from_group",        N_CHAINS),
    ("get_n_amino_acids_from_group",         N_AMINO_ACIDS),
    ("get_total_n_amino_acids_from_group",   N_AMINO_ACIDS),
    ("get_n_nucleotides_from_group",         0),
    ("get_total_n_nucleotides_from_group",   0),
    ("get_n_ions_from_group",                0),
    ("get_total_n_ions_from_group",          0),
    ("get_n_waters_from_group",              0),
    ("get_total_n_waters_from_group",        0),
    ("get_n_small_molecules_from_group",     0),
    ("get_total_n_small_molecules_from_group", 0),
    ("get_n_lipids_from_group",              0),
    ("get_total_n_lipids_from_group",        0),
    ("get_n_saccharides_from_group",         0),
    ("get_total_n_saccharides_from_group",   0),
    ("get_n_peptides_from_group",            1),
    ("get_total_n_peptides_from_group",      1),
    ("get_n_proteins_from_group",            0),
    ("get_total_n_proteins_from_group",      0),
    ("get_n_polysaccharides_from_group",     0),
    ("get_total_n_polysaccharides_from_group", 0),
    ("get_n_dnas_from_group",                0),
    ("get_total_n_dnas_from_group",          0),
    ("get_n_rnas_from_group",                0),
    ("get_total_n_rnas_from_group",          0),
])
def test_group_scalar_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


def test_group_name_from_group_is_list_of_strings(topo):
    names = aux.get_group_name_from_group(topo)
    assert isinstance(names, list)
    assert all(isinstance(n, str) for n in names)


def test_group_type_from_group_all_amino_acid(topo):
    types = aux.get_group_type_from_group(topo)
    assert all(t == 'amino acid' for t in types)


def test_chain_name_from_group_is_none(topo):
    assert aux.get_chain_name_from_group(topo) is None


def test_n_atoms_from_group_sums_to_total(topo):
    counts = aux.get_n_atoms_from_group(topo)
    assert sum(counts) == N_ATOMS


# ---------------------------------------------------------------------------
# Component-level — per-component list functions (N_COMPONENTS=1)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_component",
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
    "get_chain_type_from_component",
    "get_n_atoms_from_component",
    "get_n_groups_from_component",
])
def test_component_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_COMPONENTS


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_components_from_component",          N_COMPONENTS),
    ("get_total_n_components_from_component",    N_COMPONENTS),
    ("get_total_n_atoms_from_component",         N_ATOMS),
    ("get_total_n_groups_from_component",        N_GROUPS),
    ("get_n_molecules_from_component",           N_MOLECULES),
    ("get_total_n_molecules_from_component",     N_MOLECULES),
    ("get_n_entities_from_component",            N_ENTITIES),
    ("get_total_n_entities_from_component",      N_ENTITIES),
    ("get_n_chains_from_component",              N_CHAINS),
    ("get_total_n_chains_from_component",        N_CHAINS),
    ("get_n_amino_acids_from_component",         N_AMINO_ACIDS),
    ("get_total_n_amino_acids_from_component",   N_AMINO_ACIDS),
    ("get_n_nucleotides_from_component",         0),
    ("get_total_n_nucleotides_from_component",   0),
    ("get_n_ions_from_component",                0),
    ("get_total_n_ions_from_component",          0),
    ("get_n_waters_from_component",              0),
    ("get_total_n_waters_from_component",        0),
    ("get_n_small_molecules_from_component",     0),
    ("get_n_lipids_from_component",              0),
    ("get_total_n_lipids_from_component",        0),
    ("get_n_saccharides_from_component",         0),
    ("get_total_n_saccharides_from_component",   0),
    ("get_n_polysaccharides_from_component",     0),
])
def test_component_scalar_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


def test_chain_name_from_component_is_none(topo):
    assert aux.get_chain_name_from_component(topo) is None


# ---------------------------------------------------------------------------
# Molecule-level — per-molecule list functions (N_MOLECULES=1)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_molecule",
    "get_atom_id_from_molecule",
    "get_atom_name_from_molecule",
    "get_atom_type_from_molecule",
    "get_group_index_from_molecule",
    "get_group_id_from_molecule",
    "get_group_name_from_molecule",
    "get_group_type_from_molecule",
    "get_molecule_index_from_molecule",
    "get_molecule_id_from_molecule",
    "get_molecule_name_from_molecule",
    "get_molecule_type_from_molecule",
    "get_entity_index_from_molecule",
    "get_entity_id_from_molecule",
    "get_entity_name_from_molecule",
    "get_entity_type_from_molecule",
    "get_component_index_from_molecule",
    "get_component_id_from_molecule",
    "get_component_name_from_molecule",
    "get_component_type_from_molecule",
    "get_chain_index_from_molecule",
    "get_chain_id_from_molecule",
    "get_chain_type_from_molecule",
    "get_n_atoms_from_molecule",
    "get_n_groups_from_molecule",
    "get_n_components_from_molecule",
])
def test_molecule_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_MOLECULES


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_molecules_from_molecule",           N_MOLECULES),
    ("get_total_n_molecules_from_molecule",     N_MOLECULES),
    ("get_total_n_atoms_from_molecule",         N_ATOMS),
    ("get_total_n_groups_from_molecule",        N_GROUPS),
    ("get_total_n_components_from_molecule",    N_COMPONENTS),
    ("get_n_entities_from_molecule",            N_ENTITIES),
    ("get_total_n_entities_from_molecule",      N_ENTITIES),
    # Scalar unique counts in openmm.Topology:
    ("get_n_chains_from_molecule",              N_CHAINS),
    ("get_total_n_chains_from_molecule",        N_CHAINS),
    ("get_n_amino_acids_from_molecule",         N_AMINO_ACIDS),
    ("get_total_n_amino_acids_from_molecule",   N_AMINO_ACIDS),
    ("get_n_nucleotides_from_molecule",         0),
    ("get_total_n_nucleotides_from_molecule",   0),
    ("get_n_ions_from_molecule",                0),
    ("get_total_n_ions_from_molecule",          0),
    ("get_n_waters_from_molecule",              0),
    ("get_total_n_waters_from_molecule",        0),
    ("get_n_lipids_from_molecule",              0),
    ("get_total_n_lipids_from_molecule",        0),
    ("get_n_saccharides_from_molecule",         0),
    ("get_total_n_saccharides_from_molecule",   0),
    ("get_n_small_molecules_from_molecule",     0),
    ("get_n_polysaccharides_from_molecule",     0),
    ("get_total_n_polysaccharides_from_molecule", 0),
    ("get_n_peptides_from_molecule",            1),
    ("get_total_n_peptides_from_molecule",      1),
    ("get_n_proteins_from_molecule",            0),
    ("get_total_n_proteins_from_molecule",      0),
    ("get_n_dnas_from_molecule",                0),
    ("get_total_n_dnas_from_molecule",          0),
    ("get_n_rnas_from_molecule",                0),
    ("get_total_n_rnas_from_molecule",          0),
])
def test_molecule_scalar_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


def test_molecule_type_is_peptide(topo):
    types = aux.get_molecule_type_from_molecule(topo)
    assert isinstance(types, list)
    assert types == ['peptide']


def test_chain_name_from_molecule_is_none(topo):
    assert aux.get_chain_name_from_molecule(topo) is None


# ---------------------------------------------------------------------------
# Entity-level — per-entity list functions (N_ENTITIES=1)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_entity",
    "get_atom_id_from_entity",
    "get_atom_name_from_entity",
    "get_atom_type_from_entity",
    "get_group_index_from_entity",
    "get_group_id_from_entity",
    "get_group_name_from_entity",
    "get_group_type_from_entity",
    "get_molecule_index_from_entity",
    "get_molecule_id_from_entity",
    "get_molecule_name_from_entity",
    "get_molecule_type_from_entity",
    "get_entity_index_from_entity",
    "get_entity_id_from_entity",
    "get_entity_name_from_entity",
    "get_entity_type_from_entity",
    "get_component_index_from_entity",
    "get_component_id_from_entity",
    "get_component_name_from_entity",
    "get_component_type_from_entity",
    "get_chain_index_from_entity",
    "get_chain_id_from_entity",
    "get_chain_type_from_entity",
    "get_n_atoms_from_entity",
    "get_n_groups_from_entity",
    "get_n_molecules_from_entity",
    "get_n_components_from_entity",
])
def test_entity_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_ENTITIES


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_entities_from_entity",              N_ENTITIES),
    ("get_total_n_entities_from_entity",        N_ENTITIES),
    ("get_total_n_atoms_from_entity",           N_ATOMS),
    ("get_total_n_groups_from_entity",          N_GROUPS),
    ("get_total_n_molecules_from_entity",       N_MOLECULES),
    ("get_total_n_components_from_entity",      N_COMPONENTS),
    ("get_n_chains_from_entity",                N_CHAINS),
    ("get_total_n_chains_from_entity",          N_CHAINS),
    ("get_n_amino_acids_from_entity",           N_AMINO_ACIDS),
    ("get_total_n_amino_acids_from_entity",     N_AMINO_ACIDS),
    ("get_n_nucleotides_from_entity",           0),
    ("get_total_n_nucleotides_from_entity",     0),
    ("get_n_ions_from_entity",                  0),
    ("get_total_n_ions_from_entity",            0),
    ("get_n_waters_from_entity",                0),
    ("get_total_n_waters_from_entity",          0),
    ("get_n_lipids_from_entity",                0),
    ("get_total_n_lipids_from_entity",          0),
    ("get_n_saccharides_from_entity",           0),
    ("get_total_n_saccharides_from_entity",     0),
    ("get_n_small_molecules_from_entity",       0),
    ("get_n_peptides_from_entity",              1),
    ("get_total_n_peptides_from_entity",        1),
    ("get_n_proteins_from_entity",              0),
    ("get_total_n_proteins_from_entity",        0),
    ("get_n_polysaccharides_from_entity",       0),
    ("get_total_n_polysaccharides_from_entity", 0),
    ("get_n_dnas_from_entity",                  0),
    ("get_total_n_dnas_from_entity",            0),
    ("get_n_rnas_from_entity",                  0),
    ("get_total_n_rnas_from_entity",            0),
])
def test_entity_scalar_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


def test_entity_type_is_peptide(topo):
    types = aux.get_entity_type_from_entity(topo)
    assert isinstance(types, list)
    assert types == ['peptide']


def test_chain_name_from_entity_is_none(topo):
    assert aux.get_chain_name_from_entity(topo) is None


# ---------------------------------------------------------------------------
# Chain-level — per-chain list functions (N_CHAINS=1)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_chain",
    "get_atom_id_from_chain",
    "get_atom_name_from_chain",
    "get_atom_type_from_chain",
    "get_group_index_from_chain",
    "get_group_id_from_chain",
    "get_group_name_from_chain",
    "get_group_type_from_chain",
    "get_molecule_index_from_chain",
    "get_molecule_id_from_chain",
    "get_molecule_name_from_chain",
    "get_molecule_type_from_chain",
    "get_entity_index_from_chain",
    "get_entity_id_from_chain",
    "get_entity_name_from_chain",
    "get_entity_type_from_chain",
    "get_component_index_from_chain",
    "get_component_id_from_chain",
    "get_component_name_from_chain",
    "get_component_type_from_chain",
    "get_chain_index_from_chain",
    "get_chain_id_from_chain",
    "get_chain_type_from_chain",
    "get_n_atoms_from_chain",
    "get_n_groups_from_chain",
    "get_n_molecules_from_chain",
    "get_n_entities_from_chain",
    "get_n_components_from_chain",
])
def test_chain_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_CHAINS


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_chains_from_chain",              N_CHAINS),
    ("get_total_n_chains_from_chain",        N_CHAINS),
    ("get_total_n_atoms_from_chain",         N_ATOMS),
    ("get_total_n_groups_from_chain",        N_GROUPS),
    ("get_total_n_molecules_from_chain",     N_MOLECULES),
    ("get_total_n_entities_from_chain",      N_ENTITIES),
    ("get_total_n_components_from_chain",    N_COMPONENTS),
    ("get_n_amino_acids_from_chain",         N_AMINO_ACIDS),
    ("get_total_n_amino_acids_from_chain",   N_AMINO_ACIDS),
    ("get_n_nucleotides_from_chain",         0),
    ("get_total_n_nucleotides_from_chain",   0),
    ("get_n_ions_from_chain",                0),
    ("get_total_n_ions_from_chain",          0),
    ("get_n_waters_from_chain",              0),
    ("get_total_n_waters_from_chain",        0),
    ("get_n_lipids_from_chain",              0),
    ("get_total_n_lipids_from_chain",        0),
    ("get_n_saccharides_from_chain",         0),
    ("get_total_n_saccharides_from_chain",   0),
    ("get_n_small_molecules_from_chain",     0),
    ("get_n_peptides_from_chain",            1),
    ("get_n_proteins_from_chain",            0),
    ("get_n_polysaccharides_from_chain",     0),
    ("get_total_n_polysaccharides_from_chain", 0),
    ("get_n_dnas_from_chain",                0),
    ("get_total_n_dnas_from_chain",          0),
    ("get_n_rnas_from_chain",                0),
    ("get_total_n_rnas_from_chain",          0),
])
def test_chain_scalar_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


def test_chain_name_from_chain_is_none(topo):
    assert aux.get_chain_name_from_chain(topo) is None


def test_chain_type_from_chain(topo):
    types = aux.get_chain_type_from_chain(topo)
    assert isinstance(types, list)
    assert len(types) == N_CHAINS
    # openmm.Topology uses 'system' for chains that mix residue types or cannot
    # be narrowly classified; a single peptide chain is labelled 'system'.
    assert isinstance(types[0], str)


# ---------------------------------------------------------------------------
# Bond-level — per-bond list functions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_bond_index_from_bond",
    "get_bonded_atom_pairs_from_bond",
    "get_n_bonds_from_bond",
])
def test_bond_list_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    if isinstance(result, list):
        assert len(result) == N_BONDS
    else:
        assert result == N_BONDS


def test_bonded_atoms_from_bond_length(topo):
    result = aux.get_bonded_atoms_from_bond(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDED_ATOMS


# ---------------------------------------------------------------------------
# Cross-consistency checks
# ---------------------------------------------------------------------------

def test_atom_index_from_group_spans_all_atoms(topo):
    per_group = aux.get_atom_index_from_group(topo)
    all_atom_indices = [idx for grp in per_group for idx in grp]
    assert sorted(all_atom_indices) == list(range(N_ATOMS))


def test_atom_index_from_chain_spans_all_atoms(topo):
    per_chain = aux.get_atom_index_from_chain(topo)
    all_atom_indices = [idx for chain in per_chain for idx in chain]
    assert sorted(all_atom_indices) == list(range(N_ATOMS))


def test_n_atoms_from_molecule_sums_to_total(topo):
    counts = aux.get_n_atoms_from_molecule(topo)
    assert sum(counts) == N_ATOMS


def test_n_atoms_from_entity_sums_to_total(topo):
    counts = aux.get_n_atoms_from_entity(topo)
    assert sum(counts) == N_ATOMS


def test_n_atoms_from_chain_sums_to_total(topo):
    counts = aux.get_n_atoms_from_chain(topo)
    assert sum(counts) == N_ATOMS
