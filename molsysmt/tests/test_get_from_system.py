import pytest
from molsysmt.multitool import _get_form as get_form
from molsysmt import get
from molsysmt import convert
import numpy as np
import pickle

with open('data/1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

args = [
    'data/1tcd.pdb',
    convert('data/1tcd.pdb', to_form='molsysmt.MolSys'),
    convert('data/1tcd.pdb', to_form='molsysmt.Topology'),
    convert('data/1tcd.pdb', to_form='openmm.Topology'),
    convert('data/1tcd.pdb', to_form='openmm.Modeller'),
    convert('data/1tcd.pdb', to_form='pdbfixer.PDBFixer')
]


# System

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_atoms_from_system(item):
    output = get(item, target='system', n_atoms=True)
    assert output==expected_values['n_atoms_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_groups_from_system(item):
    output = get(item, target='system', n_groups=True)
    assert output==expected_values['n_groups_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_components_from_system(item):
    output = get(item, target='system', n_components=True)
    assert output==expected_values['n_components_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_chains_from_system(item):
    output = get(item, target='system', n_chains=True)
    assert output==expected_values['n_chains_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_molecules_from_system(item):
    output = get(item, target='system', n_molecules=True)
    assert output==expected_values['n_molecules_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_entities_from_system(item):
    output = get(item, target='system', n_entities=True)
    assert output==expected_values['n_entities_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_bonds_from_system(item):
    output = get(item, target='system', n_bonds=True)
    assert output==expected_values['n_bonds_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_aminoacids_from_system(item):
    output = get(item, target='system', n_aminoacids=True)
    assert output==expected_values['n_aminoacids_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_nucleotides_from_system(item):
    output = get(item, target='system', n_nucleotides=True)
    assert output==expected_values['n_nucleotides_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_ions_from_system(item):
    output = get(item, target='system', n_ions=True)
    assert output==expected_values['n_ions_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_waters_from_system(item):
    output = get(item, target='system', n_waters=True)
    assert output==expected_values['n_waters_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_cosolutes_from_system(item):
    output = get(item, target='system', n_cosolutes=True)
    assert output==expected_values['n_cosolutes_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_small_molecules_from_system(item):
    output = get(item, target='system', n_small_molecules=True)
    assert output==expected_values['n_small_molecules_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_peptides_from_system(item):
    output = get(item, target='system', n_peptides=True)
    assert output==expected_values['n_peptides_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_proteins_from_system(item):
    output = get(item, target='system', n_proteins=True)
    assert output==expected_values['n_proteins_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_dnas_from_system(item):
    output = get(item, target='system', n_dnas=True)
    assert output==expected_values['n_dnas_from_system']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_rnas_from_system(item):
    output = get(item, target='system', n_rnas=True)
    assert output==expected_values['n_rnas_from_system']

