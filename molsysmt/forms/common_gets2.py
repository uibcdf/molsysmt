from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt import MolSys as _molsysmt_MolSys
import simtk.unit as unit

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molsysmt_MolSys : form_name,
    'molsysmt.MolSys': form_name
}

info=["",""]
with_topology=True
with_trajectory=True

def to_molsysmt_MolSys(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_molsysmt_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

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
        return np.array(indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    group_index_from_atom = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_index_from_atom)
    group_ids = get_group_id_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_ids))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_atom)
    del(aux_dict)
    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    group_index_from_atom = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_index_from_atom)
    group_names = get_group_name_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_names))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_atom)
    del(aux_dict)
    return output

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    group_index_from_atom = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_index_from_atom)
    group_types = get_group_type_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_types))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_atom)
    del(aux_dict)
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

   from molsysmt.elements.component import get_elements

   output, _, _, _ = get_elements(item)

   if indices is not 'all':
       output = output[indices]

   return output

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_ids = get_component_id_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_ids))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_types = get_component_type_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_types))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    chain_index_from_atom = get_chain_index_from_atom(item, indices=indices)
    chain_indices = np.unique(chain_index_from_atom)
    chain_ids = get_chain_id_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_ids))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_atom)
    del(aux_dict)
    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    chain_index_from_atom = get_chain_index_from_atom(item, indices=indices)
    chain_indices = np.unique(chain_index_from_atom)
    chain_names = get_chain_name_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_names))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_atom)
    del(aux_dict)
    return output

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    chain_index_from_atom = get_chain_index_from_atom(item, indices=indices)
    chain_indices = np.unique(chain_index_from_atom)
    chain_types = get_chain_type_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_types))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_atom)
    del(aux_dict)
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_atom)
    molecule_ids = get_molecule_id_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_ids))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_atom)
    del(aux_dict)
    return output

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_atom)
    molecule_names = get_molecule_name_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_names))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_atom)
    del(aux_dict)
    return output

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_atom)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_types))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_atom)
    del(aux_dict)
    return output

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices=indices)
    entity_indices = np.unique(entity_index_from_atom)
    entity_ids = get_entity_id_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(molecule_indices, entity_ids))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_atom)
    del(aux_dict)
    return output

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices=indices)
    entity_indices = np.unique(entity_index_from_atom)
    entity_names = get_entity_name_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_names))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_atom)
    del(aux_dict)
    return output

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices=indices)
    entity_indices = np.unique(entity_index_from_atom)
    entity_types = get_entity_type_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_types))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_atom)
    del(aux_dict)
    return output

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

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_bond_index_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    if indices is 'all':
        return get_n_bonds_from_system (item)
    else:
        raise NotImplementedError

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):     # EMPTY

    if indices is 'all':
        return get_n_inner_bonds_from_system (item)
    else:
        raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):     # EMPTY

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

    group_index_from_atom = get_group_index_from_atom(item, indices='all')

    if indices is 'all':
        n_groups = get_n_groups_from_system(item)
        indices = np.arange(n_groups)

    output = []
    for group_index in indices:
        atom_indices = np.where(group_index_from_atom==group_index)
        output.append(atom_indices)

    output = np.array(output)

    return output

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group(item, indices=indices)
    atom_indices = np.unique(atom_index_from_atom)
    atom_ids = get_atom_id_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_ids))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_group)
    del(aux_dict)
    return output

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group(item, indices=indices)
    atom_indices = np.unique(atom_index_from_atom)
    atom_names = get_atom_names_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_names))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_group)
    del(aux_dict)
    return output

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group(item, indices=indices)
    atom_indices = np.unique(atom_index_from_atom)
    atom_types = get_atom_types_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_types))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_group)
    del(aux_dict)
    return output

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_groups = get_n_groups_from_system()
        output = np.arange(n_groups)
    else:
        output = np.arange(indices)
    return output

def get_group_id_from_group(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices)
    first_atom_index_from_group = np.array([ii[0] for ii in atom_index_from_group])
    output = get_component_index_from_atom (item, indices=first_atom_index_from_group)
    return output

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    component_index_from_group = get_component_index_from_group(item, indices=indices)
    component_indices = np.unique(component_index_from_group)
    component_ids = get_component_id_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_ids))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_group)
    del(aux_dict)
    return output

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    component_index_from_group = get_component_index_from_group(item, indices=indices)
    component_indices = np.unique(component_index_from_group)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_group)
    del(aux_dict)
    return output

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    component_index_from_group = get_component_index_from_group(item, indices=indices)
    component_indices = np.unique(component_index_from_group)
    component_types = get_component_type_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_types))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_group)
    del(aux_dict)
    return output

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices)
    first_atom_index_from_group = np.array([ii[0] for ii in atom_index_from_group])
    output = get_chain_index_from_atom (item, indices=first_atom_index_from_group)
    return output

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    chain_index_from_group = get_chain_index_from_group(item, indices=indices)
    chain_indices = np.unique(chain_index_from_group)
    chain_ids = get_chain_id_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_ids))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_group)
    del(aux_dict)
    return output

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    chain_index_from_group = get_chain_index_from_group(item, indices=indices)
    chain_indices = np.unique(chain_index_from_group)
    chain_names = get_chain_name_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_names))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_group)
    del(aux_dict)
    return output

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    chain_index_from_group = get_chain_index_from_group(item, indices=indices)
    chain_indices = np.unique(chain_index_from_group)
    chain_types = get_chain_type_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_types))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_group)
    del(aux_dict)
    return output

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices)
    first_atom_index_from_group = np.array([ii[0] for ii in atom_index_from_group])
    output = get_molecule_index_from_atom (item, indices=first_atom_index_from_group)
    return output

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    molecule_index_from_group = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_group)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_types))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_group)
    del(aux_dict)
    return output

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    molecule_index_from_group = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_group)
    molecule_names = get_molecule_name_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_names))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_group)
    del(aux_dict)
    return output

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    molecule_index_from_group = get_molecule_index_from_group(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_group)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_types))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_group)
    del(aux_dict)
    return output

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices)
    first_atom_index_from_group = np.array([ii[0] for ii in atom_index_from_group])
    output = get_entity_index_from_atom (item, indices=first_atom_index_from_group)
    return output

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    entity_index_from_group = get_entity_index_from_group(item, indices=indices)
    entity_indices = np.unique(entity_index_from_group)
    entity_ids = get_entity_id_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_ids))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_group)
    del(aux_dict)
    return output

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    entity_index_from_group = get_entity_index_from_group(item, indices=indices)
    entity_indices = np.unique(entity_index_from_group)
    entity_names = get_entity_name_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_names))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_group)
    del(aux_dict)
    return output

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    entity_index_from_group = get_entity_index_from_group(item, indices=indices)
    entity_indices = np.unique(entity_index_from_group)
    entity_types = get_entity_type_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_types))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_group)
    del(aux_dict)
    return output

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        output = get_atom_index_from_group (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_group_index_from_group (item, indices=indices)
        return output.shape[0]

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_group (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_bonds_from_system (item)
    else:
        output = get_molecule_index_from_group (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_group (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_group (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

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

    component_index_from_atom = get_component_index_from_atom(item, indices='all')

    if indices is 'all':
        n_components = get_n_components_from_system(item)
        indices = np.arange(n_components)

    output = []
    for component_index in indices:
        atom_indices = np.where(component_index_from_atom==component_index)
        output.append(atom_indices)

    output = np.array(output)

    return output

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component(item, indices=indices)
    atom_indices = np.unique(atom_index_from_component)
    atom_ids = get_atom_id_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_ids))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_component)
    del(aux_dict)
    return output

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component(item, indices=indices)
    atom_indices = np.unique(atom_index_from_component)
    atom_names = get_atom_name_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_names))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_component)
    del(aux_dict)
    return output

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component(item, indices=indices)
    atom_indices = np.unique(atom_index_from_component)
    atom_types = get_atom_type_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_types))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_component)
    del(aux_dict)
    return output

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    component_index_from_group = get_component_index_from_group(item, indices='all')

    if indices is 'all':
        n_components = get_n_components_from_system(item)
        indices = np.arange(n_components)

    output = []
    for component_index in indices:
        atom_indices = np.where(component_index_from_atom==component_index)
        output.append(atom_indices)

    output = np.array(output)

    return output

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    group_index_from_component = get_group_index_from_component(item, indices=indices)
    group_indices = np.unique(group_index_from_component)
    group_ids = get_group_id_from_atom(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_ids))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_component)
    del(aux_dict)
    return output

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    group_index_from_component = get_group_index_from_component(item, indices=indices)
    group_indices = np.unique(group_index_from_component)
    group_names = get_group_name_from_atom(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_names))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_component)
    del(aux_dict)
    return output

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    group_index_from_component = get_group_index_from_component(item, indices=indices)
    group_indices = np.unique(group_index_from_component)
    group_types = get_group_type_from_atom(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_types))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_component)
    del(aux_dict)
    return output

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_components = get_n_components_from_system()
        output = np.arange(n_components)
    else:
        output = np.arange(indices)
    return output

def get_component_id_from_component (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_component_name_from_component (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError


def get_component_type_from_component (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices)
    first_atom_index_from_component = np.array([ii[0] for ii in atom_index_from_component])
    output = get_chain_index_from_atom (item, indices=first_atom_index_from_component)
    return output

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    chain_index_from_component = get_chain_index_from_component(item, indices=indices)
    chain_indices = np.unique(chain_index_from_component)
    chain_ids = get_chain_id_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_ids))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_component)
    del(aux_dict)
    return output

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    chain_index_from_component = get_chain_index_from_component(item, indices=indices)
    chain_indices = np.unique(chain_index_from_component)
    chain_names = get_chain_name_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_names))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_component)
    del(aux_dict)
    return output

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    chain_index_from_component = get_chain_index_from_component(item, indices=indices)
    chain_indices = np.unique(chain_index_from_component)
    chain_types = get_chain_type_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_types))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_component)
    del(aux_dict)
    return output

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices)
    first_atom_index_from_component = np.array([ii[0] for ii in atom_index_from_component])
    output = get_molecule_index_from_atom (item, indices=first_atom_index_from_component)
    return output

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    molecule_index_from_component = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_component)
    molecule_ids = get_molecule_id_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_ids))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_component)
    del(aux_dict)
    return output

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    molecule_index_from_component = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_component)
    molecule_names = get_molecule_name_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_names))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_component)
    del(aux_dict)
    return output

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    molecule_index_from_component = get_molecule_index_from_component(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_component)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_names))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_component)
    del(aux_dict)
    return output

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices)
    first_atom_index_from_component = np.array([ii[0] for ii in atom_index_from_component])
    output = get_entity_index_from_atom (item, indices=first_atom_index_from_component)
    return output

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    entity_index_from_component = get_entity_index_from_component(item, indices=indices)
    entity_indices = np.unique(entity_index_from_component)
    entity_ids = get_entity_id_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_ids))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_component)
    del(aux_dict)
    return output

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    entity_index_from_component = get_entity_index_from_component(item, indices=indices)
    entity_indices = np.unique(entity_index_from_component)
    entity_names = get_entity_name_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_names))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_component)
    del(aux_dict)
    return output

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    entity_index_from_component = get_entity_index_from_component(item, indices=indices)
    entity_indices = np.unique(entity_index_from_component)
    entity_types = get_entity_type_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_types))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_component)
    del(aux_dict)
    return output

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        output = get_atom_index_from_component (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_atom_index_from_component (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_component (item, indices=indices)
        return output.shape[0]

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecule_index_from_molecule (item, indices=indices)
        return output.shape[0]

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_component (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_component (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

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

    molecule_index_from_atom = get_molecule_index_from_atom(item, indices='all')

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        indices = np.arange(n_molecules)

    output = []
    for molecule_index in indices:
        tmp_indices = np.where(molecule_index_from_atom==molecule_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule(item, indices=indices)
    atom_indices = np.unique(atom_index_from_molecule)
    atom_ids = get_atom_id_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_ids))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_molecule)
    del(aux_dict)
    return output

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule(item, indices=indices)
    atom_indices = np.unique(atom_index_from_molecule)
    atom_names = get_atom_name_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_names))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_molecule)
    del(aux_dict)
    return output

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule(item, indices=indices)
    atom_indices = np.unique(atom_index_from_molecule)
    atom_types = get_atom_type_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_types))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_molecule)
    del(aux_dict)
    return output

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    molecule_index_from_group = get_molecule_index_from_group(item, indices='all')

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        indices = np.arange(n_molecules)

    output = []
    for molecule_index in indices:
        tmp_indices = np.where(molecule_index_from_group==molecule_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    group_index_from_molecule = get_group_index_from_molecule(item, indices=indices)
    group_indices = np.unique(group_index_from_molecule)
    group_ids = get_group_id_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_ids))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_molecule)
    del(aux_dict)
    return output

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    group_index_from_molecule = get_group_index_from_molecule(item, indices=indices)
    group_indices = np.unique(group_index_from_molecule)
    group_names = get_group_name_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_names))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_molecule)
    del(aux_dict)
    return output

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    group_index_from_molecule = get_group_index_from_molecule(item, indices=indices)
    group_indices = np.unique(group_index_from_molecule)
    group_types = get_group_type_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_types))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_molecule)
    del(aux_dict)
    return output

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    molecule_index_from_component = get_molecule_index_from_component(item, indices='all')

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        indices = np.arange(n_molecules)

    output = []
    for molecule_index in indices:
        tmp_indices = np.where(molecule_index_from_component==molecule_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    component_index_from_molecule = get_component_index_from_molecule(item, indices=indices)
    component_indices = np.unique(component_index_from_molecule)
    component_types = get_component_type_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_types))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_molecule)
    del(aux_dict)
    return output

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    component_index_from_molecule = get_component_index_from_molecule(item, indices=indices)
    component_indices = np.unique(component_index_from_molecule)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_molecule)
    del(aux_dict)
    return output

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    component_index_from_molecule = get_component_index_from_molecule(item, indices=indices)
    component_indices = np.unique(component_index_from_molecule)
    component_types = get_component_type_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_types))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_molecule)
    del(aux_dict)
    return output

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    chain_index = get_chain_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(_unique(chain_index[mask]))

    output = _array(output)

    return output

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    chain_index_from_molecule = get_chain_index_from_molecule(item, indices=indices)
    chain_indices = np.unique(chain_index_from_molecule)
    chain_types = get_chain_type_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_types))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_molecule)
    del(aux_dict)
    return output

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    chain_index_from_molecule = get_chain_index_from_molecule(item, indices=indices)
    chain_indices = np.unique(chain_index_from_molecule)
    chain_names = get_chain_name_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_names))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_molecule)
    del(aux_dict)
    return output

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    chain_index_from_molecule = get_chain_index_from_molecule(item, indices=indices)
    chain_indices = np.unique(chain_index_from_molecule)
    chain_types = get_chain_type_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_types))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_molecule)
    del(aux_dict)
    return output

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        output = np.arange(n_molecules)
    else:
        output = np.arange(indices)
    return output

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices)
    first_atom_index_from_molecule = np.array([ii[0] for ii in atom_index_from_molecule])
    output = get_entity_index_from_atom (item, indices=first_atom_index_from_molecule)
    return output

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    entity_index_from_molecule = get_entity_index_from_molecule(item, indices=indices)
    entity_indices = np.unique(entity_index_from_molecule)
    entity_ids = get_entity_id_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_ids))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_molecule)
    del(aux_dict)
    return output

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    entity_index_from_molecule = get_entity_index_from_molecule(item, indices=indices)
    entity_indices = np.unique(entity_index_from_molecule)
    entity_names = get_entity_name_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_names))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_molecule)
    del(aux_dict)
    return output

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    entity_index_from_molecule = get_entity_index_from_molecule(item, indices=indices)
    entity_indices = np.unique(entity_index_from_molecule)
    entity_types = get_entity_type_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_types))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_molecule)
    del(aux_dict)
    return output

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        output = get_atom_index_from_molecule (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_group_index_from_molecule (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_molecule (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecule_index_from_molecule(item, indices='all')
        return output.shape[0]

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_molecule (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_molecule (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

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

    chain_index_from_atom = get_chain_index_from_atom(item, indices='all')

    if indices is 'all':
        n_chains = get_n_chains_from_system(item)
        indices = np.arange(n_chains)

    output = []
    for chain_index in indices:
        tmp_indices = np.where(chain_index_from_atom==chain_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain(item, indices=indices)
    atom_indices = np.unique(atom_index_from_chain)
    atom_ids = get_atom_id_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_ids))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_chain)
    del(aux_dict)
    return output

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain(item, indices=indices)
    atom_indices = np.unique(atom_index_from_chain)
    atom_names = get_atom_name_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_names))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_chain)
    del(aux_dict)
    return output

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain(item, indices=indices)
    atom_indices = np.unique(atom_index_from_chain)
    atom_types = get_atom_type_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_types))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_chain)
    del(aux_dict)
    return output

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    chain_index_from_group = get_chain_index_from_group(item, indices='all')

    if indices is 'all':
        n_chains = get_n_chains_from_system(item)
        indices = np.arange(n_chains)

    output = []
    for chain_index in indices:
        tmp_indices = np.where(chain_index_from_group==chain_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    group_index_from_chain = get_group_index_from_chain(item, indices=indices)
    group_indices = np.unique(group_index_from_chain)
    group_ids = get_group_id_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_ids))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_chain)
    del(aux_dict)
    return output

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    group_index_from_chain = get_group_index_from_chain(item, indices=indices)
    group_indices = np.unique(group_index_from_chain)
    group_names = get_group_name_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_names))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_chain)
    del(aux_dict)
    return output

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    group_index_from_chain = get_group_index_from_chain(item, indices=indices)
    group_indices = np.unique(group_index_from_chain)
    group_types = get_group_type_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_types))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_chain)
    del(aux_dict)
    return output

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    chain_index_from_component = get_chain_index_from_component(item, indices='all')

    if indices is 'all':
        n_chains = get_n_chains_from_system(item)
        indices = np.arange(n_chains)

    output = []
    for chain_index in indices:
        tmp_indices = np.where(chain_index_from_component==chain_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    component_index_from_chain = get_component_index_from_chain(item, indices=indices)
    component_indices = np.unique(component_index_from_chain)
    component_ids = get_component_id_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_ids))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_chain)
    del(aux_dict)
    return output

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    component_index_from_chain = get_component_index_from_chain(item, indices=indices)
    component_indices = np.unique(component_index_from_chain)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_chain)
    del(aux_dict)
    return output

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    component_index_from_chain = get_component_index_from_chain(item, indices=indices)
    component_indices = np.unique(component_index_from_chain)
    component_types = get_component_type_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_types))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_chain)
    del(aux_dict)
    return output

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_chains = get_n_chains_from_system(item)
        output = np.arange(n_chains)
    else:
        output = np.array(indices)
    return output

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    molecule_index = get_molecule_index_from_atom(item, indices='all')
    chain_indices = get_chain_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (chain_indices==ii)
        output.append(_unique(molecule_index[mask]))

    output = _array(output)

    return output

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    molecule_index_from_chain = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_chain)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_types))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_chain)
    del(aux_dict)
    return output

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    molecule_index_from_chain = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_chain)
    molecule_names = get_molecule_name_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_names))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_chain)
    del(aux_dict)
    return output

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    molecule_index_from_chain = get_molecule_index_from_chain(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_chain)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_types))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_chain)
    del(aux_dict)
    return output

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices)
    first_atom_index_from_chain = np.array([ii[0] for ii in atom_index_from_chain])
    output = get_entity_index_from_atom (item, indices=first_atom_index_from_chain)
    return output

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    entity_index_from_chain = get_entity_index_from_chain(item, indices=indices)
    entity_indices = np.unique(entity_index_from_chain)
    entity_ids = get_entity_id_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_ids))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_chain)
    del(aux_dict)
    return output

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    entity_index_from_chain = get_entity_index_from_chain(item, indices=indices)
    entity_indices = np.unique(entity_index_from_chain)
    entity_names = get_entity_name_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_names))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_chain)
    del(aux_dict)
    return output

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    entity_index_from_chain = get_entity_index_from_chain(item, indices=indices)
    entity_indices = np.unique(entity_index_from_chain)
    entity_types = get_entity_type_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_types))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_chain)
    del(aux_dict)
    return output

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        output = get_atom_index_from_chain (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_group_index_from_chain (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_component_index_from_chain (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecule_index_from_chain (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chain_index_from_chain (item, indices)
        return output.shape[0]

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_chain (item, indices=indices)
        output = np.unique(output)
        return output.shape[0]

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

    entity_index_from_atom = get_entity_index_from_atom(item, indices='all')

    if indices is 'all':
        n_entities = get_n_entities_from_system(item)
        indices = np.arange(n_entities)

    output = []
    for entity_index in indices:
        tmp_indices = np.where(entity_index_from_atom==entity_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity(item, indices=indices)
    atom_indices = np.unique(atom_index_from_entity)
    atom_ids = get_atom_id_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_ids))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_entity)
    del(aux_dict)
    return output

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity(item, indices=indices)
    atom_indices = np.unique(atom_index_from_entity)
    atom_names = get_atom_name_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_names))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_entity)
    del(aux_dict)
    return output

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity(item, indices=indices)
    atom_indices = np.unique(atom_index_from_entity)
    atom_types = get_atom_type_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_types))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_entity)
    del(aux_dict)
    return output

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    entity_index_from_group = get_entity_index_from_group(item, indices='all')

    if indices is 'all':
        n_entities = get_n_entities_from_system(item)
        indices = np.arange(n_entities)

    output = []
    for entity_index in indices:
        tmp_indices = np.where(entity_index_from_group==entity_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    group_index_from_entity = get_group_index_from_entity(item, indices=indices)
    group_indices = np.unique(group_index_from_entity)
    group_ids = get_group_id_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_ids))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_entity)
    del(aux_dict)
    return output

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    group_index_from_entity = get_group_index_from_entity(item, indices=indices)
    group_indices = np.unique(group_index_from_entity)
    group_names = get_group_name_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_names))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_entity)
    del(aux_dict)
    return output

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    group_index_from_entity = get_group_index_from_entity(item, indices=indices)
    group_indices = np.unique(group_index_from_entity)
    group_types = get_group_type_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_types))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_entity)
    del(aux_dict)
    return output

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    entity_index_from_component = get_entity_index_from_component(item, indices='all')

    if indices is 'all':
        n_entities = get_n_entities_from_system(item)
        indices = np.arange(n_entities)

    output = []
    for entity_index in indices:
        tmp_indices = np.where(entity_index_from_component==entity_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    component_index_from_entity = get_component_index_from_entity(item, indices=indices)
    component_indices = np.unique(component_index_from_entity)
    component_ids = get_component_id_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_ids))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_entity)
    del(aux_dict)
    return output

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    component_index_from_entity = get_component_index_from_entity(item, indices=indices)
    component_indices = np.unique(component_index_from_entity)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_entity)
    del(aux_dict)
    return output

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    component_index_from_entity = get_component_index_from_entity(item, indices=indices)
    component_indices = np.unique(component_index_from_entity)
    component_types = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_types))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_entity)
    del(aux_dict)
    return output

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    entity_index_from_chain = get_entity_index_from_chain(item, indices='all')

    if indices is 'all':
        n_entities = get_n_entities_from_system(item)
        indices = np.arange(n_entities)

    output = []
    for entity_index in indices:
        tmp_indices = np.where(entity_index_from_chain==entity_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    chain_index_from_entity = get_chain_index_from_entity(item, indices=indices)
    chain_indices = np.unique(chain_index_from_entity)
    chain_ids = get_chain_id_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_ids))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_entity)
    del(aux_dict)
    return output

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    chain_index_from_entity = get_chain_index_from_entity(item, indices=indices)
    chain_indices = np.unique(chain_index_from_entity)
    chain_names = get_chain_name_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_names))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_entity)
    del(aux_dict)
    return output

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    chain_index_from_entity = get_chain_index_from_entity(item, indices=indices)
    chain_indices = np.unique(chain_index_from_entity)
    chain_types = get_chain_type_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_types))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_entity)
    del(aux_dict)
    return output

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    entity_index_from_molecule = get_entity_index_from_molecule(item, indices='all')

    if indices is 'all':
        n_entities = get_n_entities_from_system(item)
        indices = np.arange(n_entities)

    output = []
    for entity_index in indices:
        tmp_indices = np.where(entity_index_from_molecule==entity_index)
        output.append(tmp_indices)

    output = np.array(output)

    return output

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    molecule_index_from_entity = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_entity)
    molecule_ids = get_molecule_id_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_ids))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_entity)
    del(aux_dict)
    return output

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    molecule_index_from_entity = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_entity)
    molecule_names = get_molecule_name_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_names))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_entity)
    del(aux_dict)
    return output

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    molecule_index_from_entity = get_molecule_index_from_entity(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_entity)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_types))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_entity)
    del(aux_dict)
    return output

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_entities = get_n_entities_from_system(item)
        output = np.arange(n_entities)
    else:
        output = np.array(indices)

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        output = get_atom_index_from_entity (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_groups_from_system (item)
    else:
        output = get_groups_index_from_entity (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_components_from_system (item)
    else:
        output = get_components_index_from_entity (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_molecules_from_system (item)
    else:
        output = get_molecules_index_from_entity (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_chains_from_system (item)
    else:
        output = get_chains_index_from_entity (item, indices=indices)
        output = [ii.shape[0] for ii in output]
        output = np.array(output)
        return output

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_entities_from_system (item)
    else:
        output = get_entity_index_from_entity (item)
        return output.shape[0]

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_groups_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_components_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_chains_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_entities_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    group_types = get_group_type_from_group(item, indices='all')
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    group_types = get_group_type_from_group(item, indices='all')
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='ion').sum()

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='small_molecule').sum()

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='rna').sum()

def get_n_lipids_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='lipid').sum()

def get_coordinates_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_box_shape_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_step_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_frame_from_system(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_system(item, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_system(item, indices='all', frame_indices='all'):     # EMPTY

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

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

    raise NotImplementedError

def get_n_bonds_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

