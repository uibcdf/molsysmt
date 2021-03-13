from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from MDAnalysis.core.topology import Topology as _mdanalysis_Topology

form_name='mdanalysis.Topology'

is_form={
    _mdanalysis_Topology : form_name,
    'mdanalysis.Topology' : form_name
        }

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_bonds=True
with_parameters=False
with_simulation=False

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

###### Get

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    output = item.ids.values
    if indices is not 'all':
        output = output[indices]
    return output

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    output = item.names.values
    if indices is not 'all':
        output = output[indices]
    return output

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    output = item.types.values
    if indices is not 'all':
        output = output[indices]
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_atoms = get_n_atoms_from_system(item)
        indices = np.arange(n_atoms)

    output = item.tt.atoms2residues(indices)

    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_index_from_atom as _get
    return _get(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_atoms = get_n_atoms_from_system(item)
        indices = np.arange(n_atoms)

    output = item.tt.atoms2segments(indices)

    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_index_from_atom as _get
    return _get(item, indices=indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_index_from_atom as _get
    return _get(item, indices=indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_inner_bonds_from_system (item)
    else:
        raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_id_from_component as get
    return get(item, indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_name_from_component as get
    return get(item, indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_type_from_component as get
    return get(item, indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_id_from_molecule as get
    return get(item, indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_name_from_molecule as get
    return get(item, indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_type_from_component as get
    return get(item, indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_id_from_molecule as get
    return get(item, indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_name_from_molecule as get
    return get(item, indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_type_from_molecule as get
    return get(item, indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.n_residues

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    output = get_component_index_from_atom(item, indices='all')
    if output[0] is None:
        n_components = 0
    else:
        output = np.unique(output)
        n_components = output.shape[0]
    return n_components

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item.n_segments

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_atom(item, indices='all')
    if output[0] is None:
        n_molecules = 0
    else:
        output = np.unique(output)
        n_molecules = output.shape[0]
    return n_molecules

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return len(item.bonds.values)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_step_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

