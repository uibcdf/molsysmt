from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy
from simtk.openmm.app import AmberInpcrdFile as _openmm_AmberInpcrdFile
from molsysmt import puw

form_name='openmm.AmberInpcrdFile'

is_form={
    _openmm_AmberInpcrdFile : form_name,
    'openmm.AmberInpcrdFile' : form_name
}

info=["",""]
with_topology=False
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False

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

##### Get

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

    xyz = item.getPositions(asNumpy=True)

    unit = puw.get_unit(xyz)

    xyz = np.expand_dims(xyz, axis=0)

    if frame_indices is not 'all':
        xyz = xyz[frame_indices, :, :]
    if indices is not 'all':
        xyz = xyz[:, indices, :]


    xyz = puw.standardize(xyz*unit)

    return xyz

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

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

    n_atoms = item.getPositions(asNumpy=True).shape[0]

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

    box = getBoxVectors(asNumpy=True)
    unit = puw.get_unit(box)
    box = np.expand_dims(box, axis=0)
    box = puw.standardize(box*unit)

    return box

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise None

def get_step_from_system(item, indices='all', frame_indices='all'):

    raise None

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 1

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    return with_box

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    return with_bonds

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

