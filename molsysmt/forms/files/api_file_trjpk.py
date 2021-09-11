import numpy as np
from molsysmt.forms.common_gets import *
from molsysmt._private_tools.exceptions import *
from molsysmt import puw
import sys
import importlib
from molsysmt.native.molecular_system import molecular_system_components
from molsysmt._private_tools.files_and_directories import tmp_filename
import pickle as pickle

form_name='file:trjpk'

is_form = {
        'file:trjpk': form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates', 'box']:
    has[ii]=True


def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    #from molsysmt.native.io.trajectory.topology import from_file_msmpk as  file_msmpk_to_molsysmt_Trajectory

    #tmp_item, tmp_molecular_system = file_msmpk_to_molsysmt_Trajectory(item,
    #        molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    #return tmp_item, tmp_molecular_system

    raise NotImplementedError

def to_molsysmt_TrajectoryDict(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item={}

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    coordinates = pickle.load(fff)
    box = pickle.load(fff)
    time = pickle.load(fff)
    step = pickle.load(fff)
    fff.close()

    if coordinates is not None:
        if frame_indices is not 'all':
            coordinates = coordinates[frame_indices, :, :]
        if atom_indices is not 'all':
            coordinates = coordinates[:, atom_indices, :]
        coordinates = puw.quantity(coordinates, unit='nm')

    if box is not None:
        if frame_indices is not 'all':
            box = box[frame_indices, :, :]
        box = puw.quantity(box, unit='nm')

    if time is not None:
        if frame_indices is not 'all':
            time = time[frame_indices]
        time = puw.quantity(time, unit='ps')

    if step is not None:
        if frame_indices is not 'all':
            step = step[frame_indices, :, :]

    tmp_item['coordinates'] = coordinates
    tmp_item['box'] = box
    tmp_item['time'] = time
    tmp_item['step'] = step

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_file_trjpk(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None, copy_if_all=False):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item, output_filename=output_filename)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=output_filename)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all', output_filename=None):

    if output_filename is None:
        output_filename = tmp_filename(extension='mmtf')

    if (atom_indices is 'all') and (frame_indices is 'all'):
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError


## Atom

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

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    coordinates = pickle.load(fff)
    fff.close()

    if coordinates is not None:
        if frame_indices is not 'all':
            coordinates = coordinates[frame_indices, :, :]
        if indices is not 'all':
            coordinates = coordinates[:, indices, :]
        coordinates = puw.quantity(coordinates, to_unit='nm')

    return coordinates

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    coordinates = pickle.load(fff)
    box = pickle.load(fff)
    time = pickle.load(fff)
    step = pickle.load(fff)
    fff.close()

    if coordinates is not None:
        if frame_indices is not 'all':
            coordinates = coordinates[frame_indices, :, :]
        if indices is not 'all':
            coordinates = coordinates[:, indices, :]
        coordinates = puw.quantity(coordinates, to_unit='nm')

    if box is not None:
        if frame_indices is not 'all':
            box = box[frame_indices, :, :]
        box = puw.quantity(box, to_unit='nm')

    if time is not None:
        if frame_indices is not 'all':
            time = time[frame_indices]
        time = puw.quantity(time, to_unit='ps')

    if step is not None:
        if frame_indices is not 'all':
            step = step[frame_indices, :, :]

    return step, time, coordinates, box

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

# System

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    fff = open(item, 'rb')
    n_atoms = pickle.load(fff)
    fff.close()

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

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    box = pickle.load(fff)
    fff.close()

    if box is not None:
        if frame_indices is not 'all':
            box = box[frame_indices, :, :]

        box = puw.quantity(box, to_unit='nm')

    return box

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_shape_from_box_vectors

    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    shape = box_shape_from_box_vectors(box)

    return shape

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_shape_from_box_vectors

    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    lengths = box_shape_from_box_vectors(box)

    return lengths

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_angles_from_box_vectors

    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    angles = box_angles_from_box_vectors(box)

    return angles

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_volume_from_box_vectors

    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    volume = box_volume_from_box_vectors(box)

    return volume

def get_time_from_system(item, indices='all', frame_indices='all'):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    time = pickle.load(fff)
    fff.close()

    if time is not None:
        if frame_indices is not 'all':
            time = time[frame_indices]

        time = puw.quantity(time, to_unit='nm')

    return time

def get_step_from_system(item, indices='all', frame_indices='all'):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    step = pickle.load(fff)
    fff.close()

    if step is not None:
        if frame_indices is not 'all':
            step = step[frame_indices]

    return step

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    n_frames = pickle.load(fff)
    fff.close()

    return n_frames

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

