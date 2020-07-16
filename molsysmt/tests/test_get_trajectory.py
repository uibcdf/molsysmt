import pytest
from molsysmt.multitool import _get_form as get_form
from molsysmt import get
from molsysmt import convert
import numpy as np
import pickle

with open('data/1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

item_pdb_file = 'data/1tcd.pdb'
item_molsysmt_MolSys = convert('data/1tcd.pdb', to_form='molsysmt.MolSys')
item_molsysmt_Trajectory = convert('data/1tcd.pdb', to_form='molsysmt.Trajectory')
item_openmm_Modeller = convert('data/1tcd.pdb', to_form='openmm.Modeller')
item_openmm_PDBFile = convert('data/1tcd.pdb', to_form='openmm.PDBFile')
item_pdbfixer_PDBFixer = convert('data/1tcd.pdb', to_form='pdbfixer.PDBFixer')

args = [
    item_pdb_file,
    item_molsysmt_MolSys,
    item_molsysmt_Trajectory,
    item_openmm_Modeller,
    item_openmm_PDBFile,
    item_pdbfixer_PDBFixer
]

# n_frames

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_frames_from_atom_1(item):
    output = get(item, target='atom', frame_indices='all', n_frames=True)
    assert output==expected_values['n_frames_from_atom_1']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_frames_from_atom_2(item):
    output = get(item, target='atom', frame_indices=0, n_frames=True)
    assert output==expected_values['n_frames_from_atom_2']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_frames_from_system_1(item):
    output = get(item, target='system', frame_indices='all', n_frames=True)
    assert output==expected_values['n_frames_from_system_1']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_frames_from_system_2(item):
    output = get(item, target='system', frame_indices=0, n_frames=True)
    assert output==expected_values['n_frames_from_system_2']

# coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_1(item):
    output = get(item, target='atom', frame_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_2(item):
    output = get(item, target='atom', frame_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_3(item):
    output = get(item, target='atom', indices=range(20,30), frame_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_3'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_1(item):
    output = get(item, target='system', frame_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_2(item):
    output = get(item, target='system', frame_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_2'])

# coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_1(item):
    output = get(item, target='atom', frame_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_2(item):
    output = get(item, target='atom', frame_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_3(item):
    output = get(item, target='atom', indices=range(20,30), frame_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_3'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_1(item):
    output = get(item, target='system', frame_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_2(item):
    output = get(item, target='system', frame_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_2'])

# step

@pytest.mark.parametrize("item", args, ids=get_form)
def test_step_from_system_1(item):
    output = get(item, target='system', frame_indices='all', step=True)
    assert np.all(output==expected_values['step_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_step_from_system_2(item):
    output = get(item, target='system', frame_indices=0, step=True)
    assert np.all(output==expected_values['step_from_system_2'])

# time

@pytest.mark.parametrize("item", args, ids=get_form)
def test_time_from_system_1(item):
    output = get(item, target='system', frame_indices='all', time=True)
    assert np.all(output==expected_values['time_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_time_from_system_2(item):
    output = get(item, target='system', frame_indices=0, time=True)
    assert np.all(output==expected_values['time_from_system_2'])




