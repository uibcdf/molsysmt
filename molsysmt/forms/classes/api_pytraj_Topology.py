from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from pytraj import Topology as _pytraj_Topology
import numpy as np

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _pytraj_Topology : form_name,
    'pytraj.Topology': form_name
}

info=["",""]
with_topology=True
with_trajectory=False

def to_molsysmt_MolSys(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_molsysmt_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_pytraj_Topology as molsysmt_Topology_from_pytraj_Topology
    from molsysmt.forms.classes.api_molsysmt_Topology import extract as extract_molsysmt_Topology
    tmp_item = molsysmt_Topology_from_pytraj_Topology(item)
    tmp_item = extract_molsysmt_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

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

def merge_two_items(item1, item2):

    raise NotImplementedError

def to_nglview(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

###### Get

## atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_atoms = get_n_atoms_from_system(item)
        return np.arange(n_atoms)
    else:
        return indices

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [None for atom in item.atoms]
    else:
        output = [None for ii in indices]
    output = np.array(output)
    return output

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [atom.name for atom in item.atoms]
    else:
        output = [item.atom(ii).name for ii in indices]
    output = np.array(output, dtype=object)
    return output

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [atom.type for atom in item.atoms]
    else:
        output = [item.atom(ii).type for ii in indices]
    output = np.array(output, dtype=object)
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [atom.resid for atom in item.atoms]
    else:
        output = [item.atom(ii).resid for ii in indices]
    output = np.array(output)
    return output

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [item.residue(atom.resid).original_resid for atom in item.atoms]
    else:
        output = [item.residue(item.atom(ii).resid).original_resid for ii in indices]
    output = np.array(output)
    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [atom.resname for atom in item.atoms]
    else:
        output = [item.atom(ii).resname for ii in indices]
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.group import name_to_type as group_name_to_group_type
    group_names = get_group_name_from_atom(item, indices=indices, frame_indices=frame_indices)
    output = [group_name_to_group_type(name) for name in group_names]
    output = np.array(output, dtype=object)
    return output

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    _, _, output, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

   from molsysmt.elements.component import get_elements

   output, _, _, _ = get_elements(item)

   if indices is not 'all':
       output = output[indices]

   return output

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    _, output, _, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    _, _, _, output = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [atom.chain for atom in item.atoms]
    else:
        output = [item.atom(ii).chain for ii in indices]
    output = np.array(output)
    return output

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [None for atom in item.atoms]
    else:
        output = [None for ii in indices]
    output = np.array(output)
    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [None for atom in item.atoms]
    else:
        output = [None for ii in indices]
    output = np.array(output)
    return output

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [None for atom in item.atoms]
    else:
        output = [None for ii in indices]
    output = np.array(output)
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output = [atom.molnum for atom in item.atoms]
    else:
        output = [item.atom(ii).molnum for ii in indices]
    output = np.array(output)
    return output

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    molecule_ids = get_molecule_id_from_molecule(item, indices='all')
    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    output = [molecule_ids[ii] for ii in molecule_index_from_atom]
    output = np.array(output)
    return output

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    molecule_names = get_molecule_name_from_molecule(item, indices='all')
    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    output = [molecule_names[ii] for ii in molecule_index_from_atom]
    output = np.array(output)
    return output

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    output = get_molecule_index_from_atom(item, indices=indices)
    output = [molecule_types[ii] for ii in output]
    output = np.array(output)
    return output

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        return indices.shape[0]

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_group_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecule_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_atom (item, indices=indices, frame_indices=frame_indices)
        output = np.unique(output)
        return output.shape[0]

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_bonds_from_system (item)
    else:
        raise NotImplementedError

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    return get_n_frames_from_system(item, indices='all', frame_indices='all')

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group (item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group (item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        raise NotImplementedError

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        raise NotImplementedError

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_bonds_from_system (item)
    else:
        raise NotImplementedError

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        raise NotImplementedError

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        raise NotImplementedError

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component (item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component (item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        raise NotImplementedError

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        raise NotImplementedError

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        raise NotImplementedError

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        raise NotImplementedError

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        raise NotImplementedError

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        raise NotImplementedError

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        raise NotImplementedError

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        raise NotImplementedError

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        raise NotImplementedError

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.n_residues

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    try:
        n_bonds = item.bond_indices.shape[0]
    except:
        n_bonds = 0

    return n_bonds

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

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

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_step_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_frame_from_system(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_system(item, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## bond

def get_index_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_index_from_bond(item, indices=indices)

def get_order_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_order_from_bond(item, indices=indices)

def get_type_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_type_from_bond(item, indices=indices)

def get_bond_index_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    output = None

    if indices is 'all':
        output = item.bond_indices
    else:
        output = item.bond_indices[indices]

    return output

def get_n_bonds_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

