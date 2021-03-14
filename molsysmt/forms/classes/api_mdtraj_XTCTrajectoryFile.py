import numpy as np
from molsysmt.forms.common_gets import *
from molsysmt._private_tools.exceptions import *
from mdtraj.formats.xtc import XTCTrajectoryFile as _mdtraj_XTCTrajectoryFile
from molsysmt import puw
from molsysmt.molecular_system import molecular_system_components

form_name='mdtraj.XTCTrajectoryFile'

is_form={
    _mdtraj_XTCTrajectoryFile: form_name,
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates', 'box']:
    has[ii]=True

def select_with_Amber(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

#### Get

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt._private_tools.math import serie_to_chunks

    if frame_indices is 'all':

        n_frames= get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    starts_serie_frames, size_serie_frames = serie_to_chunks(frame_indices)

    xyz_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        if indices is 'all':
            xyz, _, _, _ = item.read(n_frames=size)
        else:
            xyz, _, _, _ = item.read(n_frames=size, atom_indices=indices)
        xyz_list.append(xyz)

    xyz = np.concatenate(xyz_list)
    del(xyz_list)

    xyz = xyz.astype('float64')

    xyz = xyz*puw.unit(item.distance_unit)
    xyz = puw.standardize(xyz)

    return xyz


def get_frame_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt._private_tools.math import serie_to_chunks

    if frame_indices is 'all':

        n_frames= get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    starts_serie_frames, size_serie_frames = serie_to_chunks(frame_indices)

    xyz_list = []
    time_list = []
    step_list = []
    box_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        if indices is 'all':
            xyz, time, step, box = item.read(n_frames=size)
        else:
            xyz, time, step, box = item.read(n_frames=size, atom_indices=indices)
        xyz_list.append(xyz)
        time_list.append(time)
        step_list.append(step)
        box_list.append(box)

    xyz = np.concatenate(xyz_list)
    del(xyz_list)
    time = np.concatenate(time_list)
    del(time_list)
    step = np.concatenate(step_list)
    del(step_list)
    box = np.concatenate(box_list)
    del(box_list)

    xyz = xyz.astype('float64')
    box = box.astype('float64')
    time = time.astype('float64')
    step = step.astype('int64')

    xyz = xyz*puw.unit(item.distance_unit)
    xyz = puw.standardize(xyz)
    box = box*puw.unit(item.distance_unit)
    box = puw.standardize(box)
    time = time*puw.unit('ps')
    time = puw.standardize(time)

    return step, time, xyz, box

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

## system

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    position = item.tell()
    xyz, _, _, _ = item.read(n_frames=1)
    n_atoms = xyz.shape[1]
    del(xyz)
    item.seek(position)
    return n_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_box_from_system(item, indices='all', frame_indices='all'):

    from molsysmt._private_tools.math import serie_to_chunks

    if frame_indices is 'all':

        n_frames= get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    starts_serie_frames, size_serie_frames = serie_to_chunks(frame_indices)

    box_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        _, _, _, box = item.read(n_frames=size)
        box_list.append(box)

    box = np.concatenate(box_list)
    del(box_list)

    box = box.astype('float64')

    box = box*puw.unit(item.distance_unit)
    box = puw.standardize(box)

    return box

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    from molsysmt._private_tools.math import serie_to_chunks

    if frame_indices is 'all':

        n_frames= get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    starts_serie_frames, size_serie_frames = serie_to_chunks(frame_indices)

    time_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        _, time, _, _ = item.read(n_frames=size)
        time_list.append(time)

    time = np.concatenate(time_list)
    del(time_list)

    time = time.astype('float64')

    time = time*puw.unit('ps')
    time = puw.standardize(time)

    return time

def get_step_from_system(item, indices='all', frame_indices='all'):

    from molsysmt._private_tools.math import serie_to_chunks

    if frame_indices is 'all':

        n_frames= get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    starts_serie_frames, size_serie_frames = serie_to_chunks(frame_indices)

    step_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        _, _, step, _ = item.read(n_frames=size)
        step_list.append(step)

    step = np.concatenate(step_list)
    del(step_list)

    step = step.astype('int64')

    return step

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        return len(item.offsets)
    else:
        return len(frame_indices)

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

