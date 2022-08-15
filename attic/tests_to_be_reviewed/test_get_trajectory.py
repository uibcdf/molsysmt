import pytest
from molsysmt.multitool import get_form as get_form
from molsysmt import get
from molsysmt import convert
import numpy as np
import pickle

with open('data/1tcd.pickle', 'rb') as f:
    expected_values = pickle.load(f)

item_pdb_file = 'data/1tcd.pdb'
item_molsysmt_MolSys = convert('data/1tcd.pdb', to_form='molsysmt.MolSys')
item_molsysmt_Structures = convert('data/1tcd.pdb', to_form='molsysmt.Trajectory')
item_openmm_Modeller = convert('data/1tcd.pdb', to_form='openmm.Modeller')
item_openmm_PDBFile = convert('data/1tcd.pdb', to_form='openmm.PDBFile')
item_pdbfixer_PDBFixer = convert('data/1tcd.pdb', to_form='pdbfixer.PDBFixer')

args = [
    item_pdb_file,
    item_molsysmt_MolSys,
    item_molsysmt_Structures,
    item_openmm_Modeller,
    item_openmm_PDBFile,
    item_pdbfixer_PDBFixer
]

# n_structures

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_structures_from_atom_1(item):
    output = get(item, target='atom', structure_indices='all', n_structures=True)
    assert output==expected_values['n_structures_from_atom_1']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_structures_from_atom_2(item):
    output = get(item, target='atom', structure_indices=0, n_structures=True)
    assert output==expected_values['n_structures_from_atom_2']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_structures_from_system_1(item):
    output = get(item, target='system', structure_indices='all', n_structures=True)
    assert output==expected_values['n_structures_from_system_1']

@pytest.mark.parametrize("item", args, ids=get_form)
def test_n_structures_from_system_2(item):
    output = get(item, target='system', structure_indices=0, n_structures=True)
    assert output==expected_values['n_structures_from_system_2']

# coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_1(item):
    output = get(item, target='atom', structure_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_2(item):
    output = get(item, target='atom', structure_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_3(item):
    output = get(item, target='atom', indices=range(20,30), structure_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_3'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_1(item):
    output = get(item, target='system', structure_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_2(item):
    output = get(item, target='system', structure_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_2'])

# coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_1(item):
    output = get(item, target='atom', structure_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_2(item):
    output = get(item, target='atom', structure_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_2'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_atom_3(item):
    output = get(item, target='atom', indices=range(20,30), structure_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_atom_3'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_1(item):
    output = get(item, target='system', structure_indices='all', coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_coordinates_from_system_2(item):
    output = get(item, target='system', structure_indices=0, coordinates=True)
    assert np.all(output==expected_values['coordinates_from_system_2'])

# step

@pytest.mark.parametrize("item", args, ids=get_form)
def test_step_from_system_1(item):
    output = get(item, target='system', structure_indices='all', step=True)
    assert np.all(output==expected_values['step_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_step_from_system_2(item):
    output = get(item, target='system', structure_indices=0, step=True)
    assert np.all(output==expected_values['step_from_system_2'])

# time

@pytest.mark.parametrize("item", args, ids=get_form)
def test_time_from_system_1(item):
    output = get(item, target='system', structure_indices='all', time=True)
    assert np.all(output==expected_values['time_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_time_from_system_2(item):
    output = get(item, target='system', structure_indices=0, time=True)
    assert np.all(output==expected_values['time_from_system_2'])

# box

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_from_system_1(item):
    output = get(item, target='system', structure_indices='all', box=True)
    assert np.allclose(output, expected_values['box_from_system_1'], atol=1e-05)

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_from_system_2(item):
    output = get(item, target='system', structure_indices=0, box=True)
    assert np.allclose(output, expected_values['box_from_system_2'], atol=1e-05)

# box_shape

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_shape_from_system_1(item):
    output = get(item, target='system', structure_indices='all', box_shape=True)
    assert np.all(output==expected_values['box_shape_from_system_1'])

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_shape_from_system_2(item):
    output = get(item, target='system', structure_indices=0, box_shape=True)
    assert np.all(output==expected_values['box_shape_from_system_2'])

# box_lengths

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_lengths_from_system_1(item):
    output = get(item, target='system', structure_indices='all', box_lengths=True)
    assert np.allclose(output, expected_values['box_lengths_from_system_1'], atol=1e-05)

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_lengths_from_system_2(item):
    output = get(item, target='system', structure_indices=0, box_lengths=True)
    assert np.allclose(output, expected_values['box_lengths_from_system_2'], atol=1e-05)

# box_angles

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_angles_from_system_1(item):
    output = get(item, target='system', structure_indices='all', box_angles=True)
    assert np.allclose(output, expected_values['box_angles_from_system_1'], atol=1e-05)

@pytest.mark.parametrize("item", args, ids=get_form)
def test_box_angles_from_system_2(item):
    output = get(item, target='system', structure_indices=0, box_angles=True)
    assert np.allclose(output, expected_values['box_angles_from_system_2'], atol=1e-05)

# frame

@pytest.mark.parametrize("item", args, ids=get_form)
def test_frame_from_atom_1(item):
    output = get(item, target='atom', structure_indices='all', frame=True)
    expected_output = expected_values['frame_from_atom_1']
    eq_step = np.all(output[0]==expected_output[0])
    eq_time = np.all(output[1]==expected_output[1])
    eq_coordinates = np.all(output[2]==expected_output[2])
    eq_box = np.allclose(output[3], expected_output[3], atol=1e-05)
    assert eq_step*eq_time*eq_box*eq_coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_frame_from_atom_2(item):
    output = get(item, target='atom', structure_indices=0, frame=True)
    expected_output = expected_values['frame_from_atom_2']
    eq_step = np.all(output[0]==expected_output[0])
    eq_time = np.all(output[1]==expected_output[1])
    eq_coordinates = np.all(output[2]==expected_output[2])
    eq_box = np.allclose(output[3], expected_output[3], atol=1e-05)
    assert eq_step*eq_time*eq_box*eq_coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_frame_from_atom_3(item):
    output = get(item, target='atom', indices=range(20,30), structure_indices=0, frame=True)
    expected_output = expected_values['frame_from_atom_3']
    eq_step = np.all(output[0]==expected_output[0])
    eq_time = np.all(output[1]==expected_output[1])
    eq_coordinates = np.all(output[2]==expected_output[2])
    eq_box = np.allclose(output[3], expected_output[3], atol=1e-05)
    assert eq_step*eq_time*eq_box*eq_coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_frame_from_system_1(item):
    output = get(item, target='system', structure_indices='all', frame=True)
    expected_output = expected_values['frame_from_system_1']
    eq_step = np.all(output[0]==expected_output[0])
    eq_time = np.all(output[1]==expected_output[1])
    eq_coordinates = np.all(output[2]==expected_output[2])
    eq_box = np.allclose(output[3], expected_output[3], atol=1e-05)
    assert eq_step*eq_time*eq_box*eq_coordinates

@pytest.mark.parametrize("item", args, ids=get_form)
def test_frame_from_system_2(item):
    output = get(item, target='system', structure_indices='all', frame=True)
    expected_output = expected_values['frame_from_system_2']
    eq_step = np.all(output[0]==expected_output[0])
    eq_time = np.all(output[1]==expected_output[1])
    eq_coordinates = np.all(output[2]==expected_output[2])
    eq_box = np.allclose(output[3], expected_output[3], atol=1e-05)
    assert eq_step*eq_time*eq_box*eq_coordinates
