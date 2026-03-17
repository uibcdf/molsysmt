"""
Tests for molsysmt_Topology/get_topological_attributes.py using a synthetic
system built with MolSysBuilder. Ground-truth values are known by construction.

System layout
-------------
Atoms  : 13 total (ALA×5, GLY×5, HOH×1, HOH×1, NA×1)
Groups : 5  (ALA, GLY, HOH, HOH, NA)
Chains : 2  (A=peptide, B=solvent)
Molecules: 4 (peptide, water 0, water 1, ion 0)
Entities : 3 (peptide, water, NA)
Components: 4 (each disconnected fragment = one component)
Bonds  : 9  (backbone + sidechain of ALA-GLY dipeptide)
Bonded atoms: 10 (atoms 0-9, the ALA+GLY atoms; waters/ion have no bonds)

No inter-molecular bonds, so inner-bond count equals bond count.

Note on `get_n_X_from_Y` return semantics:
- When X == Y (same element type): returns scalar total count
- When X is a sub-group of Y or varies per Y: returns per-Y list of length N_Y
- `total_n_X_from_Y` always returns scalar total
"""

import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux

N_ATOMS        = 13
N_GROUPS       = 5
N_CHAINS       = 2
N_MOLECULES    = 4
N_ENTITIES     = 3
N_COMPONENTS   = 4
N_BONDS        = 9
N_BONDED_ATOMS = 10  # atoms 0-9 participate in bonds; waters/ion have none


@pytest.fixture(scope="module")
def topo():
    b = msm.MolSysBuilder()

    ala_atoms = [b.add_atom(atom_name=n, atom_type=t)
                 for n, t in [('N', 'N'), ('CA', 'C'), ('C', 'C'), ('O', 'O'), ('CB', 'C')]]
    gly_atoms = [b.add_atom(atom_name=n, atom_type=t)
                 for n, t in [('N', 'N'), ('CA', 'C'), ('C', 'C'), ('O', 'O'), ('OXT', 'O')]]
    wat1_atoms = [b.add_atom(atom_name='O', atom_type='O')]
    wat2_atoms = [b.add_atom(atom_name='O', atom_type='O')]
    ion_atoms  = [b.add_atom(atom_name='NA', atom_type='Na')]

    g_ala  = b.add_group(ala_atoms,  group_id='1', group_name='ALA', group_type='amino acid')
    g_gly  = b.add_group(gly_atoms,  group_id='2', group_name='GLY', group_type='amino acid')
    g_wat1 = b.add_group(wat1_atoms, group_id='3', group_name='HOH', group_type='water')
    g_wat2 = b.add_group(wat2_atoms, group_id='4', group_name='HOH', group_type='water')
    g_ion  = b.add_group(ion_atoms,  group_id='5', group_name='NA',  group_type='ion')

    b.add_bond(ala_atoms[0], ala_atoms[1])   # N-CA
    b.add_bond(ala_atoms[1], ala_atoms[2])   # CA-C
    b.add_bond(ala_atoms[2], ala_atoms[3])   # C=O
    b.add_bond(ala_atoms[1], ala_atoms[4])   # CA-CB
    b.add_bond(ala_atoms[2], gly_atoms[0])   # peptide bond ALA-C→GLY-N
    b.add_bond(gly_atoms[0], gly_atoms[1])   # N-CA
    b.add_bond(gly_atoms[1], gly_atoms[2])   # CA-C
    b.add_bond(gly_atoms[2], gly_atoms[3])   # C=O
    b.add_bond(gly_atoms[2], gly_atoms[4])   # C-OXT

    b.add_chain([g_ala, g_gly],            chain_id='A', chain_name='A', chain_type='peptide')
    b.add_chain([g_wat1, g_wat2, g_ion],   chain_id='B', chain_name='B', chain_type='solvent')

    mol_pep  = b.add_molecule([g_ala, g_gly], molecule_id='0', molecule_name='peptide 0', molecule_type='peptide')
    mol_wat1 = b.add_molecule([g_wat1],        molecule_id='1', molecule_name='water 0',   molecule_type='water')
    mol_wat2 = b.add_molecule([g_wat2],        molecule_id='2', molecule_name='water 1',   molecule_type='water')
    mol_ion  = b.add_molecule([g_ion],         molecule_id='3', molecule_name='ion 0',     molecule_type='ion')

    b.add_entity([mol_pep],              entity_id='0', entity_name='peptide 0', entity_type='peptide')
    b.add_entity([mol_wat1, mol_wat2],   entity_id='1', entity_name='water',     entity_type='water')
    b.add_entity([mol_ion],              entity_id='2', entity_name='NA',        entity_type='ion')

    molsys = b.build()
    return msm.convert(molsys, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# System-level counts — exact scalar values
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name, expected", [
    ("get_n_atoms_from_system",          N_ATOMS),
    ("get_n_groups_from_system",         N_GROUPS),
    ("get_n_components_from_system",     N_COMPONENTS),
    ("get_n_molecules_from_system",      N_MOLECULES),
    ("get_n_entities_from_system",       N_ENTITIES),
    ("get_n_chains_from_system",         N_CHAINS),
    ("get_n_bonds_from_system",          N_BONDS),
    ("get_n_amino_acids_from_system",    2),
    ("get_n_nucleotides_from_system",    0),
    ("get_n_ions_from_system",           1),
    ("get_n_waters_from_system",         2),
    ("get_n_small_molecules_from_system", 0),
    ("get_n_lipids_from_system",         0),
    ("get_n_saccharides_from_system",    0),
    ("get_n_peptides_from_system",       1),
    ("get_n_proteins_from_system",       0),
    ("get_n_polysaccharides_from_system", 0),
    ("get_n_dnas_from_system",           0),
    ("get_n_rnas_from_system",           0),
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


@pytest.mark.parametrize("func_name", [
    "get_bonded_atoms_from_system",
    "get_inner_bonded_atoms_from_system",
])
def test_system_bonded_atoms_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDED_ATOMS


# ---------------------------------------------------------------------------
# Atom-level attribute arrays — list of length N_ATOMS
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
    "get_component_id_from_atom",
    "get_component_name_from_atom",
    "get_component_type_from_atom",
    "get_chain_index_from_atom",
    "get_chain_id_from_atom",
    "get_chain_name_from_atom",
    "get_chain_type_from_atom",
    "get_bond_index_from_atom",
    "get_bond_type_from_atom",
    "get_bond_order_from_atom",
    "get_bonded_atoms_from_atom",
    "get_inner_bond_index_from_atom",
    "get_n_bonds_from_atom",
    "get_n_inner_bonds_from_atom",
])
def test_atom_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_ATOMS


@pytest.mark.parametrize("func_name", [
    # These return all bond pairs (N_BONDS), not one entry per atom
    "get_bonded_atom_pairs_from_atom",
    "get_inner_bonded_atom_pairs_from_atom",
])
def test_atom_bond_pairs_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDS


def test_inner_bonded_atoms_from_atom_length(topo):
    # Returns one entry per bonded atom (skips unconnected atoms)
    result = aux.get_inner_bonded_atoms_from_atom(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDED_ATOMS


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_atoms_from_atom",            N_ATOMS),
    ("get_total_n_atoms_from_atom",      N_ATOMS),
    ("get_n_groups_from_atom",           N_GROUPS),
    ("get_total_n_groups_from_atom",     N_GROUPS),
    ("get_n_molecules_from_atom",        N_MOLECULES),
    ("get_total_n_molecules_from_atom",  N_MOLECULES),
    ("get_n_entities_from_atom",         N_ENTITIES),
    ("get_total_n_entities_from_atom",   N_ENTITIES),
    ("get_n_components_from_atom",       N_COMPONENTS),
    ("get_total_n_components_from_atom", N_COMPONENTS),
    ("get_n_chains_from_atom",           N_CHAINS),
    ("get_total_n_chains_from_atom",     N_CHAINS),
    ("get_n_amino_acids_from_atom",      2),
    ("get_total_n_amino_acids_from_atom", 2),
    ("get_n_nucleotides_from_atom",      0),
    ("get_total_n_nucleotides_from_atom", 0),
    ("get_n_ions_from_atom",             1),
    ("get_total_n_ions_from_atom",       1),
    ("get_n_waters_from_atom",           2),
    ("get_total_n_waters_from_atom",     2),
    ("get_n_small_molecules_from_atom",  0),
    ("get_total_n_small_molecules_from_atom", 0),
    ("get_n_lipids_from_atom",           0),
    ("get_total_n_lipids_from_atom",     0),
    ("get_n_saccharides_from_atom",      0),
    ("get_total_n_saccharides_from_atom", 0),
    ("get_n_peptides_from_atom",         1),
    ("get_total_n_peptides_from_atom",   1),
    ("get_n_proteins_from_atom",         0),
    ("get_total_n_proteins_from_atom",   0),
    ("get_n_polysaccharides_from_atom",  0),
    ("get_total_n_polysaccharides_from_atom", 0),
    ("get_n_dnas_from_atom",             0),
    ("get_total_n_dnas_from_atom",       0),
    ("get_n_rnas_from_atom",             0),
    ("get_total_n_rnas_from_atom",       0),
    ("get_total_n_bonds_from_atom",      N_BONDS),
    ("get_total_n_inner_bonds_from_atom", N_BONDS),
])
def test_atom_total_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


# ---------------------------------------------------------------------------
# Group-level attribute arrays — list of length N_GROUPS
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
    "get_molecule_index_from_group",
    "get_molecule_id_from_group",
    "get_molecule_name_from_group",
    "get_molecule_type_from_group",
    "get_entity_index_from_group",
    "get_entity_id_from_group",
    "get_entity_name_from_group",
    "get_entity_type_from_group",
    "get_component_index_from_group",
    "get_component_id_from_group",
    "get_component_name_from_group",
    "get_component_type_from_group",
    "get_chain_index_from_group",
    "get_chain_id_from_group",
    "get_chain_name_from_group",
    "get_chain_type_from_group",
    "get_bond_index_from_group",
    "get_bond_type_from_group",
    "get_bond_order_from_group",
    "get_bonded_atoms_from_group",
    "get_bonded_atom_pairs_from_group",
    "get_inner_bond_index_from_group",
    "get_inner_bonded_atoms_from_group",
    "get_inner_bonded_atom_pairs_from_group",
    "get_n_atoms_from_group",
    "get_n_bonds_from_group",
    "get_n_inner_bonds_from_group",
    # per-group counts (each group spans exactly 1 of each of these)
    "get_n_components_from_group",
    "get_n_chains_from_group",
])
def test_group_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_GROUPS


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_groups_from_group",            N_GROUPS),
    ("get_total_n_groups_from_group",      N_GROUPS),
    ("get_total_n_atoms_from_group",       N_ATOMS),
    ("get_n_molecules_from_group",         N_MOLECULES),
    ("get_total_n_molecules_from_group",   N_MOLECULES),
    ("get_n_entities_from_group",          N_ENTITIES),
    ("get_total_n_entities_from_group",    N_ENTITIES),
    ("get_total_n_components_from_group",  N_COMPONENTS),
    ("get_total_n_chains_from_group",      N_CHAINS),
    ("get_n_amino_acids_from_group",       2),
    ("get_total_n_amino_acids_from_group", 2),
    ("get_n_nucleotides_from_group",       0),
    ("get_total_n_nucleotides_from_group", 0),
    ("get_n_ions_from_group",              1),
    ("get_total_n_ions_from_group",        1),
    ("get_n_waters_from_group",            2),
    ("get_total_n_waters_from_group",      2),
    ("get_n_small_molecules_from_group",   0),
    ("get_total_n_small_molecules_from_group", 0),
    ("get_n_lipids_from_group",            0),
    ("get_total_n_lipids_from_group",      0),
    ("get_n_saccharides_from_group",       0),
    ("get_total_n_saccharides_from_group", 0),
    ("get_n_peptides_from_group",          1),
    ("get_total_n_peptides_from_group",    1),
    ("get_n_proteins_from_group",          0),
    ("get_total_n_proteins_from_group",    0),
    ("get_n_polysaccharides_from_group",   0),
    ("get_total_n_polysaccharides_from_group", 0),
    ("get_n_dnas_from_group",              0),
    ("get_total_n_dnas_from_group",        0),
    ("get_n_rnas_from_group",              0),
    ("get_total_n_rnas_from_group",        0),
    ("get_total_n_bonds_from_group",       N_BONDS),
    ("get_total_n_inner_bonds_from_group", N_BONDS),
])
def test_group_total_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


# ---------------------------------------------------------------------------
# Molecule-level attribute arrays — list of length N_MOLECULES
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
    "get_chain_name_from_molecule",
    "get_chain_type_from_molecule",
    "get_bond_index_from_molecule",
    "get_bond_type_from_molecule",
    "get_bond_order_from_molecule",
    "get_bonded_atoms_from_molecule",
    "get_bonded_atom_pairs_from_molecule",
    "get_inner_bond_index_from_molecule",
    "get_inner_bonded_atoms_from_molecule",
    "get_inner_bonded_atom_pairs_from_molecule",
    "get_n_atoms_from_molecule",
    "get_n_groups_from_molecule",
    "get_n_bonds_from_molecule",
    "get_n_inner_bonds_from_molecule",
    # per-molecule counts (vary per molecule)
    "get_n_components_from_molecule",
    "get_n_chains_from_molecule",
    "get_n_amino_acids_from_molecule",
    "get_n_nucleotides_from_molecule",
    "get_n_ions_from_molecule",
    "get_n_waters_from_molecule",
    "get_n_lipids_from_molecule",
    "get_n_saccharides_from_molecule",
])
def test_molecule_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_MOLECULES


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_molecules_from_molecule",       N_MOLECULES),
    ("get_total_n_molecules_from_molecule", N_MOLECULES),
    ("get_total_n_atoms_from_molecule",     N_ATOMS),
    ("get_total_n_groups_from_molecule",    N_GROUPS),
    ("get_n_entities_from_molecule",        N_ENTITIES),
    ("get_total_n_entities_from_molecule",  N_ENTITIES),
    ("get_total_n_components_from_molecule", N_COMPONENTS),
    ("get_total_n_chains_from_molecule",    N_CHAINS),
    ("get_total_n_amino_acids_from_molecule", 2),
    ("get_total_n_nucleotides_from_molecule", 0),
    ("get_total_n_ions_from_molecule",      1),
    ("get_total_n_waters_from_molecule",    2),
    ("get_total_n_lipids_from_molecule",    0),
    ("get_total_n_saccharides_from_molecule", 0),
    ("get_n_peptides_from_molecule",        1),
    ("get_total_n_peptides_from_molecule",  1),
    ("get_n_proteins_from_molecule",        0),
    ("get_total_n_proteins_from_molecule",  0),
    ("get_n_dnas_from_molecule",            0),
    ("get_total_n_dnas_from_molecule",      0),
    ("get_n_rnas_from_molecule",            0),
    ("get_total_n_rnas_from_molecule",      0),
    ("get_total_n_bonds_from_molecule",     N_BONDS),
    ("get_total_n_inner_bonds_from_molecule", N_BONDS),
])
def test_molecule_total_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


@pytest.mark.xfail(reason="get_n_polysaccharides_from_molecule has a NameError bug: 'molecule_types' is not defined")
def test_n_polysaccharides_from_molecule_bug(topo):
    aux.get_n_polysaccharides_from_molecule(topo)


# ---------------------------------------------------------------------------
# Entity-level attribute arrays — list of length N_ENTITIES
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
    "get_chain_name_from_entity",
    "get_chain_type_from_entity",
    "get_bond_index_from_entity",
    "get_bond_type_from_entity",
    "get_bond_order_from_entity",
    "get_bonded_atoms_from_entity",
    "get_bonded_atom_pairs_from_entity",
    "get_inner_bond_index_from_entity",
    "get_inner_bonded_atoms_from_entity",
    "get_inner_bonded_atom_pairs_from_entity",
    "get_n_atoms_from_entity",
    "get_n_groups_from_entity",
    "get_n_molecules_from_entity",
    "get_n_bonds_from_entity",
    "get_n_inner_bonds_from_entity",
    # per-entity counts (vary per entity)
    "get_n_components_from_entity",
    "get_n_chains_from_entity",
    "get_n_amino_acids_from_entity",
    "get_n_nucleotides_from_entity",
    "get_n_ions_from_entity",
    "get_n_waters_from_entity",
    "get_n_lipids_from_entity",
    "get_n_saccharides_from_entity",
    "get_n_peptides_from_entity",
    "get_n_proteins_from_entity",
    "get_n_polysaccharides_from_entity",
    "get_n_dnas_from_entity",
    "get_n_rnas_from_entity",
])
def test_entity_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_ENTITIES


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_entities_from_entity",          N_ENTITIES),
    ("get_total_n_entities_from_entity",    N_ENTITIES),
    ("get_total_n_atoms_from_entity",       N_ATOMS),
    ("get_total_n_groups_from_entity",      N_GROUPS),
    ("get_total_n_molecules_from_entity",   N_MOLECULES),
    ("get_total_n_components_from_entity",  N_COMPONENTS),
    ("get_total_n_chains_from_entity",      N_CHAINS),
    ("get_total_n_amino_acids_from_entity", 2),
    ("get_total_n_nucleotides_from_entity", 0),
    ("get_total_n_ions_from_entity",        1),
    ("get_total_n_waters_from_entity",      2),
    ("get_total_n_lipids_from_entity",      0),
    ("get_total_n_saccharides_from_entity", 0),
    ("get_total_n_peptides_from_entity",    1),
    ("get_total_n_proteins_from_entity",    0),
    ("get_total_n_polysaccharides_from_entity", 0),
    ("get_total_n_dnas_from_entity",        0),
    ("get_total_n_rnas_from_entity",        0),
    ("get_total_n_bonds_from_entity",       N_BONDS),
    ("get_total_n_inner_bonds_from_entity", N_BONDS),
])
def test_entity_total_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


# ---------------------------------------------------------------------------
# Component-level attribute arrays — list of length N_COMPONENTS
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
    "get_molecule_index_from_component",
    "get_molecule_id_from_component",
    "get_molecule_name_from_component",
    "get_molecule_type_from_component",
    "get_entity_index_from_component",
    "get_entity_id_from_component",
    "get_entity_name_from_component",
    "get_entity_type_from_component",
    "get_component_index_from_component",
    "get_component_id_from_component",
    "get_component_name_from_component",
    "get_component_type_from_component",
    "get_chain_index_from_component",
    "get_chain_id_from_component",
    "get_chain_name_from_component",
    "get_chain_type_from_component",
    "get_bond_index_from_component",
    "get_bond_type_from_component",
    "get_bond_order_from_component",
    "get_bonded_atoms_from_component",
    "get_bonded_atom_pairs_from_component",
    "get_inner_bond_index_from_component",
    "get_inner_bonded_atoms_from_component",
    "get_inner_bonded_atom_pairs_from_component",
    "get_n_atoms_from_component",
    "get_n_groups_from_component",
    "get_n_bonds_from_component",
    "get_n_inner_bonds_from_component",
    # per-component counts
    "get_n_chains_from_component",
    "get_n_amino_acids_from_component",
    "get_n_nucleotides_from_component",
    "get_n_ions_from_component",
    "get_n_waters_from_component",
    "get_n_lipids_from_component",
    "get_n_saccharides_from_component",
])
def test_component_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_COMPONENTS


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_components_from_component",        N_COMPONENTS),
    ("get_total_n_components_from_component",  N_COMPONENTS),
    ("get_total_n_atoms_from_component",       N_ATOMS),
    ("get_total_n_groups_from_component",      N_GROUPS),
    ("get_n_molecules_from_component",         N_MOLECULES),
    ("get_total_n_molecules_from_component",   N_MOLECULES),
    ("get_n_entities_from_component",          N_ENTITIES),
    ("get_total_n_entities_from_component",    N_ENTITIES),
    ("get_total_n_chains_from_component",      N_CHAINS),
    ("get_total_n_amino_acids_from_component", 2),
    ("get_total_n_nucleotides_from_component", 0),
    ("get_total_n_ions_from_component",        1),
    ("get_total_n_waters_from_component",      2),
    ("get_total_n_lipids_from_component",      0),
    ("get_total_n_saccharides_from_component", 0),
    ("get_total_n_bonds_from_component",       N_BONDS),
    ("get_total_n_inner_bonds_from_component", N_BONDS),
])
def test_component_total_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


# ---------------------------------------------------------------------------
# Chain-level attribute arrays — list of length N_CHAINS
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
    "get_chain_name_from_chain",
    "get_chain_type_from_chain",
    "get_bond_index_from_chain",
    "get_bond_type_from_chain",
    "get_bond_order_from_chain",
    "get_bonded_atoms_from_chain",
    "get_bonded_atom_pairs_from_chain",
    "get_inner_bond_index_from_chain",
    "get_inner_bonded_atoms_from_chain",
    "get_inner_bonded_atom_pairs_from_chain",
    "get_n_atoms_from_chain",
    "get_n_groups_from_chain",
    # per-chain counts
    "get_n_molecules_from_chain",
    "get_n_entities_from_chain",
    "get_n_components_from_chain",
    "get_n_bonds_from_chain",
    "get_n_inner_bonds_from_chain",
    "get_n_amino_acids_from_chain",
    "get_n_nucleotides_from_chain",
    "get_n_ions_from_chain",
    "get_n_waters_from_chain",
    "get_n_lipids_from_chain",
    "get_n_saccharides_from_chain",
    "get_n_peptides_from_chain",
    "get_n_proteins_from_chain",
    "get_n_polysaccharides_from_chain",
    "get_n_dnas_from_chain",
    "get_n_rnas_from_chain",
])
def test_chain_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_CHAINS


@pytest.mark.parametrize("func_name, expected", [
    ("get_n_chains_from_chain",           N_CHAINS),
    ("get_total_n_chains_from_chain",     N_CHAINS),
    ("get_total_n_atoms_from_chain",      N_ATOMS),
    ("get_total_n_groups_from_chain",     N_GROUPS),
    ("get_total_n_molecules_from_chain",  N_MOLECULES),
    ("get_total_n_entities_from_chain",   N_ENTITIES),
    ("get_total_n_components_from_chain", N_COMPONENTS),
    ("get_total_n_amino_acids_from_chain", 2),
    ("get_total_n_nucleotides_from_chain", 0),
    ("get_total_n_ions_from_chain",       1),
    ("get_total_n_waters_from_chain",     2),
    ("get_total_n_lipids_from_chain",     0),
    ("get_total_n_saccharides_from_chain", 0),
    ("get_total_n_polysaccharides_from_chain", 0),
    ("get_total_n_dnas_from_chain",       0),
    ("get_total_n_rnas_from_chain",       0),
    ("get_total_n_bonds_from_chain",      N_BONDS),
    ("get_total_n_inner_bonds_from_chain", N_BONDS),
])
def test_chain_total_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected


# ---------------------------------------------------------------------------
# Bond-level attribute arrays — list of length N_BONDS
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_bond_index_from_bond",
    "get_bond_order_from_bond",
    "get_bond_type_from_bond",
    "get_bonded_atom_pairs_from_bond",
    "get_n_bonds_from_bond",
])
def test_bond_scalar_or_list(topo, func_name):
    # n_bonds_from_bond returns scalar; bond lists return N_BONDS entries
    result = getattr(aux, func_name)(topo)
    if isinstance(result, list):
        assert len(result) == N_BONDS
    else:
        assert result == N_BONDS


def test_bonded_atoms_from_bond(topo):
    # Returns unique bonded atom indices (flat list), not one per bond
    result = aux.get_bonded_atoms_from_bond(topo)
    assert isinstance(result, list)
    assert len(result) == N_BONDED_ATOMS


# ---------------------------------------------------------------------------
# Spot-check: specific values
# ---------------------------------------------------------------------------

def test_atom_names_ala(topo):
    names = aux.get_atom_name_from_atom(topo)
    assert names[:5] == ['N', 'CA', 'C', 'O', 'CB']


def test_atom_names_gly(topo):
    names = aux.get_atom_name_from_atom(topo)
    assert names[5:10] == ['N', 'CA', 'C', 'O', 'OXT']


def test_group_names(topo):
    names = aux.get_group_name_from_group(topo)
    assert names == ['ALA', 'GLY', 'HOH', 'HOH', 'NA']


def test_chain_ids(topo):
    ids = aux.get_chain_id_from_chain(topo)
    assert ids == ['A', 'B']


def test_molecule_types(topo):
    types = aux.get_molecule_type_from_molecule(topo)
    assert types == ['peptide', 'water', 'water', 'ion']


def test_entity_types(topo):
    types = aux.get_entity_type_from_entity(topo)
    assert types == ['peptide', 'water', 'ion']


def test_atoms_per_group(topo):
    counts = aux.get_n_atoms_from_group(topo)
    assert counts == [5, 5, 1, 1, 1]


def test_atoms_per_molecule(topo):
    counts = aux.get_n_atoms_from_molecule(topo)
    assert counts == [10, 1, 1, 1]


def test_atoms_per_entity(topo):
    counts = aux.get_n_atoms_from_entity(topo)
    assert counts == [10, 2, 1]
