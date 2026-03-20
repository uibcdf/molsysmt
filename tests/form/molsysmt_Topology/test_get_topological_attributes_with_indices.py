"""
Tests for molsysmt_Topology/get_topological_attributes.py — explicit indices branch.

Every function in get_topological_attributes.py has an
    if indices == 'all': ...
    else: ...
branch. The existing test suite only exercises the 'all' path. This file
exercises the else path by passing explicit integer index lists.

The fixture reuses the same MolSysBuilder system as the builder test:
- 13 atoms, 5 groups, 2 chains, 4 molecules, 3 entities, 4 components, 9 bonds
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import get_topological_attributes as aux


def _is_scalar_number(val):
    """Accept Python int/float and numpy scalar types."""
    return isinstance(val, (int, float, np.integer, np.floating))

# ---------------------------------------------------------------------------
# Constants (same system as test_get_topological_attributes_from_builder.py)
# ---------------------------------------------------------------------------

N_ATOMS        = 13
N_GROUPS       = 5
N_CHAINS       = 2
N_MOLECULES    = 4
N_ENTITIES     = 3
N_COMPONENTS   = 4
N_BONDS        = 9


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

    b.add_bond(ala_atoms[0], ala_atoms[1])
    b.add_bond(ala_atoms[1], ala_atoms[2])
    b.add_bond(ala_atoms[2], ala_atoms[3])
    b.add_bond(ala_atoms[1], ala_atoms[4])
    b.add_bond(ala_atoms[2], gly_atoms[0])
    b.add_bond(gly_atoms[0], gly_atoms[1])
    b.add_bond(gly_atoms[1], gly_atoms[2])
    b.add_bond(gly_atoms[2], gly_atoms[3])
    b.add_bond(gly_atoms[2], gly_atoms[4])

    b.add_chain([g_ala, g_gly],           chain_id='A', chain_name='A', chain_type='peptide')
    b.add_chain([g_wat1, g_wat2, g_ion],  chain_id='B', chain_name='B', chain_type='solvent')

    mol_pep  = b.add_molecule([g_ala, g_gly], molecule_id='0', molecule_name='peptide 0', molecule_type='peptide')
    mol_wat1 = b.add_molecule([g_wat1],        molecule_id='1', molecule_name='water 0',   molecule_type='water')
    mol_wat2 = b.add_molecule([g_wat2],        molecule_id='2', molecule_name='water 1',   molecule_type='water')
    mol_ion  = b.add_molecule([g_ion],         molecule_id='3', molecule_name='ion 0',     molecule_type='ion')

    b.add_entity([mol_pep],             entity_id='0', entity_name='peptide 0', entity_type='peptide')
    b.add_entity([mol_wat1, mol_wat2],  entity_id='1', entity_name='water',     entity_type='water')
    b.add_entity([mol_ion],             entity_id='2', entity_name='NA',        entity_type='ion')

    molsys = b.build()
    return msm.convert(molsys, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SOME_ATOM_INDICES      = [0, 1, 5]       # first atom of ALA, second of ALA, first of GLY
SOME_GROUP_INDICES     = [0, 2]          # ALA group, first HOH group
SOME_MOLECULE_INDICES  = [0, 1]          # peptide, first water
SOME_ENTITY_INDICES    = [0, 2]          # peptide entity, ion entity
SOME_COMPONENT_INDICES = [0, 2]          # first two components
SOME_CHAIN_INDICES     = [0, 1]          # both chains (only 2 exist)
SOME_BOND_INDICES      = [0, 4]          # first bond (N-CA), fifth bond (peptide bond)


# ---------------------------------------------------------------------------
# Atom-level — explicit indices
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
def test_atom_list_func_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_ATOM_INDICES)
    assert isinstance(result, list)
    assert len(result) == len(SOME_ATOM_INDICES)


@pytest.mark.parametrize("func_name", [
    "get_bonded_atom_pairs_from_atom",
    "get_inner_bonded_atom_pairs_from_atom",
])
def test_atom_bond_pairs_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_ATOM_INDICES)
    assert isinstance(result, list)


def test_inner_bonded_atoms_from_atom_with_indices(topo):
    result = aux.get_inner_bonded_atoms_from_atom(topo, indices=SOME_ATOM_INDICES)
    assert isinstance(result, list)


@pytest.mark.parametrize("func_name", [
    "get_total_n_atoms_from_atom",
    "get_total_n_groups_from_atom",
    "get_total_n_molecules_from_atom",
    "get_total_n_entities_from_atom",
    "get_total_n_components_from_atom",
    "get_total_n_chains_from_atom",
    "get_total_n_bonds_from_atom",
    "get_total_n_inner_bonds_from_atom",
    "get_total_n_amino_acids_from_atom",
    "get_total_n_nucleotides_from_atom",
    "get_total_n_ions_from_atom",
    "get_total_n_waters_from_atom",
    "get_total_n_small_molecules_from_atom",
    "get_total_n_lipids_from_atom",
    "get_total_n_saccharides_from_atom",
    "get_total_n_peptides_from_atom",
    "get_total_n_proteins_from_atom",
    "get_total_n_polysaccharides_from_atom",
    "get_total_n_dnas_from_atom",
    "get_total_n_rnas_from_atom",
    "get_n_atoms_from_atom",
    "get_n_groups_from_atom",
    "get_n_molecules_from_atom",
    "get_n_entities_from_atom",
    "get_n_components_from_atom",
    "get_n_chains_from_atom",
    "get_n_amino_acids_from_atom",
    "get_n_nucleotides_from_atom",
    "get_n_ions_from_atom",
    "get_n_waters_from_atom",
    "get_n_small_molecules_from_atom",
    "get_n_lipids_from_atom",
    "get_n_saccharides_from_atom",
    "get_n_peptides_from_atom",
    "get_n_proteins_from_atom",
    "get_n_polysaccharides_from_atom",
    "get_n_dnas_from_atom",
    "get_n_rnas_from_atom",
])
def test_atom_scalar_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_ATOM_INDICES)
    assert _is_scalar_number(result)


# ---------------------------------------------------------------------------
# Group-level — explicit indices
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
    "get_n_components_from_group",
    "get_n_chains_from_group",
])
def test_group_list_func_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_GROUP_INDICES)
    assert isinstance(result, list)
    assert len(result) == len(SOME_GROUP_INDICES)


@pytest.mark.parametrize("func_name", [
    "get_n_groups_from_group",
    "get_total_n_groups_from_group",
    "get_total_n_atoms_from_group",
    "get_n_molecules_from_group",
    "get_total_n_molecules_from_group",
    "get_n_entities_from_group",
    "get_total_n_entities_from_group",
    "get_total_n_components_from_group",
    "get_total_n_chains_from_group",
    "get_total_n_bonds_from_group",
    "get_total_n_inner_bonds_from_group",
    "get_n_amino_acids_from_group",
    "get_total_n_amino_acids_from_group",
    "get_n_nucleotides_from_group",
    "get_total_n_nucleotides_from_group",
    "get_n_ions_from_group",
    "get_total_n_ions_from_group",
    "get_n_waters_from_group",
    "get_total_n_waters_from_group",
    "get_n_small_molecules_from_group",
    "get_total_n_small_molecules_from_group",
    "get_n_lipids_from_group",
    "get_total_n_lipids_from_group",
    "get_n_saccharides_from_group",
    "get_total_n_saccharides_from_group",
    "get_n_peptides_from_group",
    "get_total_n_peptides_from_group",
    "get_n_proteins_from_group",
    "get_total_n_proteins_from_group",
    "get_n_polysaccharides_from_group",
    "get_total_n_polysaccharides_from_group",
    "get_n_dnas_from_group",
    "get_total_n_dnas_from_group",
    "get_n_rnas_from_group",
    "get_total_n_rnas_from_group",
])
def test_group_scalar_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_GROUP_INDICES)
    assert _is_scalar_number(result)


# ---------------------------------------------------------------------------
# Molecule-level — explicit indices
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
    "get_n_components_from_molecule",
    "get_n_chains_from_molecule",
    "get_n_amino_acids_from_molecule",
    "get_n_nucleotides_from_molecule",
    "get_n_ions_from_molecule",
    "get_n_waters_from_molecule",
    "get_n_lipids_from_molecule",
    "get_n_saccharides_from_molecule",
])
def test_molecule_list_func_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_MOLECULE_INDICES)
    assert isinstance(result, list)
    assert len(result) == len(SOME_MOLECULE_INDICES)


@pytest.mark.parametrize("func_name", [
    "get_n_molecules_from_molecule",
    "get_total_n_molecules_from_molecule",
    "get_total_n_atoms_from_molecule",
    "get_total_n_groups_from_molecule",
    "get_n_entities_from_molecule",
    "get_total_n_entities_from_molecule",
    "get_total_n_components_from_molecule",
    "get_total_n_chains_from_molecule",
    "get_total_n_bonds_from_molecule",
    "get_total_n_inner_bonds_from_molecule",
    "get_total_n_amino_acids_from_molecule",
    "get_total_n_nucleotides_from_molecule",
    "get_total_n_ions_from_molecule",
    "get_total_n_waters_from_molecule",
    "get_total_n_lipids_from_molecule",
    "get_total_n_saccharides_from_molecule",
    "get_n_polysaccharides_from_molecule",
    "get_total_n_polysaccharides_from_molecule",
    "get_n_peptides_from_molecule",
    "get_total_n_peptides_from_molecule",
    "get_n_proteins_from_molecule",
    "get_total_n_proteins_from_molecule",
    "get_n_dnas_from_molecule",
    "get_total_n_dnas_from_molecule",
    "get_n_rnas_from_molecule",
    "get_total_n_rnas_from_molecule",
])
def test_molecule_scalar_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_MOLECULE_INDICES)
    assert _is_scalar_number(result)


# ---------------------------------------------------------------------------
# Entity-level — explicit indices
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
def test_entity_list_func_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_ENTITY_INDICES)
    assert isinstance(result, list)
    assert len(result) == len(SOME_ENTITY_INDICES)


@pytest.mark.parametrize("func_name", [
    "get_n_entities_from_entity",
    "get_total_n_entities_from_entity",
    "get_total_n_atoms_from_entity",
    "get_total_n_groups_from_entity",
    "get_total_n_molecules_from_entity",
    "get_total_n_components_from_entity",
    "get_total_n_chains_from_entity",
    "get_total_n_bonds_from_entity",
    "get_total_n_inner_bonds_from_entity",
    "get_total_n_amino_acids_from_entity",
    "get_total_n_nucleotides_from_entity",
    "get_total_n_ions_from_entity",
    "get_total_n_waters_from_entity",
    "get_total_n_lipids_from_entity",
    "get_total_n_saccharides_from_entity",
    "get_total_n_peptides_from_entity",
    "get_total_n_proteins_from_entity",
    "get_total_n_polysaccharides_from_entity",
    "get_total_n_dnas_from_entity",
    "get_total_n_rnas_from_entity",
])
def test_entity_scalar_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_ENTITY_INDICES)
    assert _is_scalar_number(result)


# ---------------------------------------------------------------------------
# Component-level — explicit indices
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
    "get_n_chains_from_component",
    "get_n_amino_acids_from_component",
    "get_n_nucleotides_from_component",
    "get_n_ions_from_component",
    "get_n_waters_from_component",
    "get_n_lipids_from_component",
    "get_n_saccharides_from_component",
])
def test_component_list_func_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_COMPONENT_INDICES)
    assert isinstance(result, list)
    assert len(result) == len(SOME_COMPONENT_INDICES)


@pytest.mark.parametrize("func_name", [
    "get_n_components_from_component",
    "get_total_n_components_from_component",
    "get_total_n_atoms_from_component",
    "get_total_n_groups_from_component",
    "get_n_molecules_from_component",
    "get_total_n_molecules_from_component",
    "get_n_entities_from_component",
    "get_total_n_entities_from_component",
    "get_total_n_chains_from_component",
    "get_total_n_bonds_from_component",
    "get_total_n_inner_bonds_from_component",
    "get_total_n_amino_acids_from_component",
    "get_total_n_nucleotides_from_component",
    "get_total_n_ions_from_component",
    "get_total_n_waters_from_component",
    "get_total_n_lipids_from_component",
    "get_total_n_saccharides_from_component",
])
def test_component_scalar_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_COMPONENT_INDICES)
    assert _is_scalar_number(result)


# ---------------------------------------------------------------------------
# Chain-level — explicit indices (subset: just chain 0)
# ---------------------------------------------------------------------------

SINGLE_CHAIN_INDEX = [0]

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
def test_chain_list_func_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SINGLE_CHAIN_INDEX)
    assert isinstance(result, list)
    assert len(result) == len(SINGLE_CHAIN_INDEX)


@pytest.mark.parametrize("func_name", [
    "get_n_chains_from_chain",
    "get_total_n_chains_from_chain",
    "get_total_n_atoms_from_chain",
    "get_total_n_groups_from_chain",
    "get_total_n_molecules_from_chain",
    "get_total_n_entities_from_chain",
    "get_total_n_components_from_chain",
    "get_total_n_bonds_from_chain",
    "get_total_n_inner_bonds_from_chain",
    "get_total_n_amino_acids_from_chain",
    "get_total_n_nucleotides_from_chain",
    "get_total_n_ions_from_chain",
    "get_total_n_waters_from_chain",
    "get_total_n_lipids_from_chain",
    "get_total_n_saccharides_from_chain",
    "get_total_n_polysaccharides_from_chain",
    "get_total_n_peptides_from_chain",
    "get_total_n_proteins_from_chain",
    "get_total_n_dnas_from_chain",
    "get_total_n_rnas_from_chain",
])
def test_chain_scalar_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SINGLE_CHAIN_INDEX)
    assert _is_scalar_number(result)


# ---------------------------------------------------------------------------
# Bond-level — explicit indices
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("func_name", [
    "get_bond_index_from_bond",
    "get_bond_order_from_bond",
    "get_bond_type_from_bond",
    "get_bonded_atom_pairs_from_bond",
])
def test_bond_list_func_with_indices(topo, func_name):
    result = getattr(aux, func_name)(topo, indices=SOME_BOND_INDICES)
    assert isinstance(result, list)
    assert len(result) == len(SOME_BOND_INDICES)


def test_n_bonds_from_bond_with_indices(topo):
    result = aux.get_n_bonds_from_bond(topo, indices=SOME_BOND_INDICES)
    assert _is_scalar_number(result)
    assert result == len(SOME_BOND_INDICES)


def test_bonded_atoms_from_bond_with_indices(topo):
    result = aux.get_bonded_atoms_from_bond(topo, indices=SOME_BOND_INDICES)
    assert isinstance(result, list)
    # Returns unique atom indices touched by the selected bonds
    assert len(result) >= 1
