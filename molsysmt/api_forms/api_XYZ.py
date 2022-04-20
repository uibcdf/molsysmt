from molsysmt._private.exceptions import *

from molsysmt.form.XYZ.is_file_XYZ import is_XYZ as is_form
from molsysmt.form.XYZ.extract import extract
from molsysmt.form.XYZ.add import add
from molsysmt.form.XYZ.append_structures import append_structures
from molsysmt.form.XYZ.get import *
from molsysmt.form.XYZ.set import *

form_name='XYZ'
form_type='class'
form_info = ["",""]

form_attributes = {

    'atom_index' : False,
    'atom_id' : False,
    'atom_name' : False,
    'atom_type' : False,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,
    'bond_order' : False,

    'group_index' : False,
    'group_id' : False,
    'group_name' : False,
    'group_type' : False,

    'component_index' : False,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : False,
    'molecule_id' : False,
    'molecule_name' : False,
    'molecule_type' : False,

    'chain_index' : False,
    'chain_id' : False,
    'chain_name' : False,
    'chain_type' : False,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : False,
    'box' : False,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_molsysmt_Structures(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.XYZ import to_molsysmt_Structures as XYZ_to_molsysmt_Structures

    tmp_item = XYZ_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_xyznpy(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.XYZ import to_file_xyznpy as XYZ_to_file_xyznpy

    tmp_item = XYZ_to_file_xyznpy(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

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

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

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



