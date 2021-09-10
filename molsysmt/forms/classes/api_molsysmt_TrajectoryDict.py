from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt import puw
from molsysmt.native.molecular_system import molecular_system_components

form_name='molsysmt.TrajectoryDict'

is_form={
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates','box']:
    has[ii]=True

def this_dict_is_TrajectoryDict(item):

    from molsysmt._private_tools.trajectory import is_trajectory_dict

    return is_trajectory_dict(item)

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_TrajectoryDict as TrajectoryDict_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = TrajectoryDict_to_molsysmt_Trajectory(item, None, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_file_trjpk(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    import pickle as pickle

    # lengths with nm values and times in ps

    if atom_indices is 'all':
        if tmp_item['coordinates'] is not None:
            n_atoms = tmp_item['coordinates'].shape[1]
        else:
            n_atoms = 0
    else:
        n_atoms = atom_indices.shape[0]

    if frame_indices is 'all':
        if tmp_item['coordinates'] is not None:
            n_frames = tmp_item['coordinates'].shape[0]
        elif tmp_item['box'] is not None:
            n_frames = tmp_item['box'].shape[0]
        elif tmp_item['time'] is not None:
            n_frames = tmp_item['time'].shape[0]
        else:
            n_frames = 0
    else:
        n_frames = frame_indices.shape[0]

    fff = open(output_filename, 'wb')

    pickle.dump(n_atoms, fff)
    pickle.dump(n_frames, fff)

    if tmp_item['coordinates'] is not None:
        coordinates = item['coordinates']
        if frame_indices is not 'all':
            coordinates = coordinates[frame_indices,:,:]
        elif atom_indices is not 'all':
            coordinates = coordinates[:,atom_indices,:]
        coordinates = puw.get_value(coordinates, to_unit='nm')
    else:
        coordinates = None

    pickle.dump(coordinates, fff)
    del(coordinates)

    if tmp_item['box'] is not None:
        box = item['box']
        if frame_indices is not 'all':
            box = box[frame_indices,:,:]
        box = puw.get_value(box, to_unit='nm')
    else:
        box = None

    pickle.dump(box, fff)
    del(box)

    if tmp_item['time'] is not None:
        time = item['time']
        if frame_indices is not 'all':
            time = time[frame_indices]
        time = puw.get_value(time, to_unit='nm')
    else:
        time = None

    pickle.dump(time, fff)
    del(time)

    if tmp_item['step'] is not None:
        step = item['step']
        if frame_indices is not 'all':
            step = step[frame_indices]
    else:
        step = None

    pickle.dump(step, fff)
    del(step)

    fff.close()

    tmp_item = output_filename

    if molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_TrajectoryDict(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        tmp_item = item.copy()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

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

    tmp_coordinates = item['coordinates']

    if frame_indices is not 'all':
        tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    if indices is not 'all':
        tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates

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

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    output = None

    if 'coordinates' in item:
        output = item['coordinates'].shape[1]

    return output

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

    output=None

    if 'box' in item:

        len_shape = len(item['box'].shape)

        if len_shape==3:
            if frame_indices is 'all':
                output=item['box']
            else:
                output=item['box'][frame_indices,:,:]
        elif len_shape==2:
            if frame_indices is 'all':
                n_frames=get_n_frames_from_system(item)
            else:
                n_frames=len(frame_indices)
            output=np.tile(item['box'], (n_frames, 1, 1))

    return output

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_shape_from_box_vectors
    output = None
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    if box is not None:
        output = box_shape_from_box_vectors(box)
    return output

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_lengths_from_box_vectors
    output = None
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    if box is not None:
        output = box_lengths_from_box_vectors(box)
    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_angles_from_box_vectors
    output = None
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    if box is not None:
        output = box_angles_from_box_vectors(box)
    return output

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_volume_from_box_vectors
    output = None
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    if box is not None:
        output = box_volume_from_box_vectors(box)
    return output

def get_time_from_system(item, indices='all', frame_indices='all'):

    output = None
    if frame_indices is 'all':
        output = item['time']
    else:
        output = item['time'][frame_indices]
    return output

def get_step_from_system(item, indices='all', frame_indices='all'):

    output = None
    if frame_indices is 'all':
        output = item['step']
    else:
        output = item['step'][frame_indices]
    return output

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    output = None

    if frame_indices is 'all':
        if 'coordinates' in item:
            output=item['coordinates'].shape[0]
        elif 'box' in item:
            len_shape = len(item['box'].shape)
            if len_shape==3:
                output=item['box'].shape[0]
            elif len_shape==2:
                output=1
    else:
        output=frame_indices.shape[0]

    return output

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

## atom

def set_coordinates_to_atom(item, indices='all', frame_indices='all', value=None):

    length_unit = puw.get_unit(item['coordinates'])
    value = puw.convert(value, to_unit=length_unit)

    if indices is 'all':
        if frame_indices is 'all':
            item['coordinates']=value
        else:
            item['coordinates'][frame_indices,:,:]=value
    else:
        if frame_indices is 'all':
            item['coordinates'][:,indices,:]=value
        else:
            item['coordinates'][np.ix_(indices,frame_indices)]=value

    pass

## system

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

