from os.path import basename as _basename
import numpy as np
from molsysmt._private_tools.exceptions import *
import simtk.unit as unit
from molsysmt.forms.common_gets import *

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
}

info=["",""]
with_topology=False
with_coordinates=True
with_box=False
with_parameters=False

def item_in_good_shape(item):

    tmp_item = item

    if type(item._value)==list:
        tmp_item = np.array(tmp_item._value)*tmp_item.unit

    if len(tmp_item.shape)==2:
        from numpy import expand_dims
        tmp_item = expand_dims(tmp_item, axis=0)*item.unit

    return tmp_item

def this_Quantity_has_XYZ_shape(item):

    # Only np.arrays of shape [n_frames, n_particles, coordinates] or [n_particles, coordinates] are
    # admitted

    has_right_shape = False

    if type(item._value)==list:
        item = np.array(item._value)*item.unit

    shape = item.shape

    if len(shape)==3 and shape[-1]==3:
        has_right_shape = True
    elif len(shape)==2 and shape[-1]==3:
        has_right_shape = True

    return has_right_shape

def this_Quantity_is_XYZ(item):

    # Only np.arrays of shape [n_frames, n_particles, coordinates] or [n_particles, coordinates] are
    # admitted

    from numpy import ndarray

    is_length = False

    list_base_dimensions = list(item.unit.iter_base_dimensions())

    if len(list_base_dimensions)==1:
        if list_base_dimensions[0][0].name == 'length':
            is_length = True

    has_right_shape = this_Quantity_has_XYZ_shape(item)

    return (has_right_shape and is_length)

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all',
                           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.classes import from_XYZ as XYZ_to_molsysmt_Trajectory

    tmp_item = XYZ_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_xyznpy(item, atom_indices='all', frame_indices='all',
              topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
              output_filename=None):

    comment = None
    atom_names = None
    xyz = None
    unit_name = None

    xyz = item._value
    unit_name = item.unit.get_name()

    with open(output_filename, 'wb') as fff:
        np.save(fff, comment)
        np.save(fff, atom_names)
        np.save(fff, unit_name)
        np.save(fff, xyz)

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def to_NGLView(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError


###### Get

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    tmp_coordinates=tmp_item[:,:,:]

    if indices is not 'all':
        tmp_coordinates = tmp_item[:,indices,:]

    if frame_indices is not 'all':
        tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    return tmp_coordinates


## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    return tmp_item.shape[1]

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    tmp_coordinates=tmp_item[:,:,:]
    if frame_indices is not 'all':
        tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    return tmp_coordinates

def get_box_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_step_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    return tmp_item.shape[0]

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    return False

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    return False

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError



