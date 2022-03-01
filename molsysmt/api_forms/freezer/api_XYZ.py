import numpy as np
from molsysmt._private_tools.exceptions import *
from molsysmt.api_forms.common_gets import *
from molsysmt import puw
from molsysmt.native.molecular_system import molecular_system_components

form_name='XYZ'
from_type='class'

is_form={
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates']:
    has[ii]=True

def item_in_good_shape(item):

    unit = puw.get_unit(item)
    value = puw.get_value(item)

    if type(value)==list:
        value = np.array(value)

    if len(value.shape)==2:
        value = np.expand_dims(value, axis=0)
    elif len(value.shape)==1:
        value = np.expand_dims(value, axis=0)
        value = np.expand_dims(value, axis=0)

    return value*unit

def this_Quantity_has_XYZ_shape(item):

    # Only np.arrays of shape [n_frames, n_particles, coordinates] or [n_particles, coordinates] are
    # admitted

    has_right_shape = False

    shape = np.shape(item)

    if len(shape)==3 and shape[-1]==3:
        has_right_shape = True
    elif len(shape)==2 and shape[-1]==3:
        has_right_shape = True
    elif len(shape)==1 and shape[-1]==3:
        has_right_shape = True

    return has_right_shape

def this_Quantity_is_XYZ(item):

    # Only np.arrays of shape [n_frames, n_particles, coordinates] or [n_particles, coordinates] are
    # admitted

    is_length = puw.compatibility(item, puw.unit('nm'))
    has_right_shape = this_Quantity_has_XYZ_shape(item)

    return (has_right_shape and is_length)

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.trajectory import from_XYZ as XYZ_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = XYZ_to_molsysmt_Trajectory(item,
            molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def to_file_xyznpy(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    tmp_item = output_filename

    with open(tmp_item, 'wb') as fff:
        np.save(fff, item.shape, allow_pickle=True)
        np.save(fff, puw.get_value(item, to_unit='nm'), allow_pickle=True)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_XYZ(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        from copy import copy
        tmp_item = copy(item)
    else:
        tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)

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

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    tmp_item = item_in_good_shape(item)
    tmp_coordinates=tmp_item[:,:,:]

    if indices is not 'all':
        tmp_coordinates = tmp_item[:,indices,:]

    if structure_indices is not 'all':
        tmp_coordinates = tmp_coordinates[structure_indices,:,:]

    return tmp_coordinates


## group

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_group_type_from_group(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

## component

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    tmp_item = item_in_good_shape(item)
    return tmp_item.shape[1]

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_coordinates_from_system(item, indices='all', structure_indices='all'):

    tmp_item = item_in_good_shape(item)
    tmp_coordinates=tmp_item[:,:,:]
    if structure_indices is not 'all':
        tmp_coordinates = tmp_coordinates[structure_indices,:,:]

    return tmp_coordinates

def get_box_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_time_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_step_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_n_frames_from_system(item, indices='all', structure_indices='all'):

    tmp_item = item_in_good_shape(item)
    return tmp_item.shape[0]

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()



