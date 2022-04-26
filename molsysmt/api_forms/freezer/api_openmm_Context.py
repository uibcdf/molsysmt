from molsysmt._private.exceptions import *
from molsysmt.api_forms.common_gets import *
import numpy as np
from molsysmt import puw
from molsysmt.native.molecular_system import molecular_system_components

form_name='openmm.Context'
from_type='class'

is_form={
    'openmm.Context' : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['box', 'coordinates', 'ff_parameters', 'mm_parameters', 'thermo_state', 'simulation']:
    has[ii]=True

def to_openmm_System(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    tmp_item = item.getSystem()
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

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
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

##### Get

# atom

def get_atom_index_from_atom(item, indices='all', structure_indices='all'):

    raise NotWithThisFormError()

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

def get_coordinates_from_atom (item, indices='all', structure_indices='all'):

    coordinates = item.getState(getPositions=True).getPositions(asNumpy=True)
    unit = puw.get_unit(coordinates)
    coordinates = puw.get_value(coordinates)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if structure_indices is not 'all':
        coordinates = coordinates[structure_indices,:,:]

    if indices is not 'all':
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates

def get_frame_from_atom(item, indices='all', structure_indices='all'):

    tmp_step = get_step_from_system(item, structure_indices=structure_indices)
    tmp_time = get_time_from_system(item, structure_indices=structure_indices)
    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, structure_indices=structure_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

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

def get_n_atoms_from_system (item, indices='all', structure_indices='all'):

    return item.getSystem().getNumParticles()

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

def get_box_from_system(item, indices='all', structure_indices='all'):

    box=item.getState().getPeriodicBoxVectors(asNumpy=True)

    if box is not None:
        box_unit = box.unit
        box = np.array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box_unit

    output=None

    if box is not None:
        if structure_indices is 'all':
            output=box
        else:
            output=box[structure_indices,:,:]

    return output

def get_box_shape_from_system (item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = box_shape_from_box_vectors(tmp_box)

    return output

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = box_lengths_from_box_vectors(tmp_box)

    return output

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = box_angles_from_box_vectors(tmp_box)

    return output

def get_box_volume_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_volume_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    if tmp_box is None:
        output=None
    else:
        output = box_volume_from_box_vectors(tmp_box)

    return output

def get_time_from_system(item, indices='all', structure_indices='all'):

    output = item.getState().getTime()
    value = puw.get_value(output)
    unit = puw.get_unit(output)
    output = np.array([value])*unit
    output = puw.standardize(output)

    return output

def get_step_from_system(item, indices='all', structure_indices='all'):

    return None

def get_n_structures_from_system (item, indices='all', structure_indices='all'):

    return 1

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

