from molsysmt._private.exceptions import *
import numpy as np

from molsysmt.form.pytraj_Trajectory.is_pytraj_Trajectory import is_pytraj_Trajectory as is_form
from molsysmt.form.pytraj_Trajectory.extract import extract
from molsysmt.form.pytraj_Trajectory.add import add
from molsysmt.form.pytraj_Trajectory.append_structures import append_structures
from molsysmt.form.pytraj_Trajectory.get import *
from molsysmt.form.pytraj_Trajectory.set import *

form_name='pytraj.Trajectory'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,
    'bond_order' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_pytraj_Topology as pytraj_Trajectory_to_pytraj_Topology

    tmp_item = pytraj_Trajectory_to_pytraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_molsysmt_MolSys as pytraj_Trajectory_to_molsysmt_MolSys

    tmp_item = pytraj_Trajectory_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Topology as pytraj_Trajectory_to_molsysmt_Topology

    tmp_item = pytraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Structures as pytraj_Trajectory_to_molsysmt_Structures

    tmp_item = pytraj_Trajectory_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                        structure_indices=structure_indices, check=False)

    return tmp_item

def extract(item, atom_indices='all', structure_indices='all'):

    raise NotImplementedError()

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

## atom

def get_index_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_id_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_name_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_type_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_atom(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_id_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_name_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_type_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_id_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_name_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_type_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_name_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_id_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_type_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_name_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_id_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_type_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_id_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_name_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_type_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_id_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_name_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_type_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_atoms_from_atom (item, indices='all', structure_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        return indices.shape[0]

def get_n_groups_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_groups_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_components_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_components_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_molecules_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_molecules_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_chains_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_chains_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_entities_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_bonded_atoms_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_bond_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_bond_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonds_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_inner_bond_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_inner_bond_index_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_inner_bonded_atoms_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_inner_bonds_from_atom as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    tmp_item = item.xyz * 0.1 * unit.nanometers
    if indices is not 'all':
        tmp_item = tmp_item[:,atom_indices,:]
    if structure_indices is not 'all':
        tmp_item = tmp_item[structure_indices,:,:]
    return tmp_item

def get_frame_from_atom(item, indices='all', structure_indices='all'):

    tmp_step = get_step_from_system(item, structure_indices=structure_indices)
    tmp_time = get_time_from_system(item, structure_indices=structure_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, structure_indices=structure_indices)
    tmp_box = get_box_from_system(item, structure_indices=structure_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_structures_from_atom(item, indices='all', structure_indices='all'):

    return get_n_structures_from_system(item, indices='all', structure_indices='all')

def get_form_from_atom(item, indices='all', structure_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', structure_indices='all'):

    return get_group_index_from_group (item, indices=indices, structure_indices=structure_indices)

def get_id_from_group (item, indices='all', structure_indices='all'):

    return get_group_id_from_group (item, indices=indices, structure_indices=structure_indices)

def get_name_from_group (item, indices='all', structure_indices='all'):

    return get_group_name_from_group (item, indices=indices, structure_indices=structure_indices)

def get_type_from_group (item, indices='all', structure_indices='all'):

    return get_group_type_from_group (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_index_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_id_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_id_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_name_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_name_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_type_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_type_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_index_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_index_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_id_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_name_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_type_from_group(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_type_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_name_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_name_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_index_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_index_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_id_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_id_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_type_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_type_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_name_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_name_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_index_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_index_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_id_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_id_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_type_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_type_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_index_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_index_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_id_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_id_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_name_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_name_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_type_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_type_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_index_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_index_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_id_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_id_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_name_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_name_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_type_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_type_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_atoms_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_atoms_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_groups_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_groups_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_components_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_components_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_molecules_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_molecules_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_chains_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_chains_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_entities_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_group (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonds_from_group as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

## component

def get_index_from_component (item, indices='all', structure_indices='all'):

    return get_component_index_from_component (item, indices=indices, structure_indices=structure_indices)

def get_id_from_component (item, indices='all', structure_indices='all'):

    return get_component_id_from_component (item, indices=indices, structure_indices=structure_indices)

def get_name_from_component (item, indices='all', structure_indices='all'):

    return get_component_name_from_component (item, indices=indices, structure_indices=structure_indices)

def get_type_from_component (item, indices='all', structure_indices='all'):

    return get_component_type_from_component (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_index_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_id_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_id_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_name_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_name_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_type_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_type_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_index_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_index_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_id_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_id_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_name_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_name_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_type_from_component(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_type_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_name_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_index_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_index_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_id_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_type_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_name_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_name_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_index_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_index_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_id_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_id_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_type_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_type_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_index_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_index_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_id_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_id_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_name_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_name_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_type_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_type_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_index_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_index_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_id_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_id_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_name_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_name_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_type_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_type_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_atoms_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_atoms_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_groups_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_groups_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_components_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_components_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_molecules_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_molecules_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_chains_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_chains_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_entities_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_component (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonds_from_component as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

## molecule

def get_index_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_id_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_name_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_type_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_index_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_id_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_id_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_name_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_name_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_type_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_type_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_index_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_index_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_id_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_id_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_name_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_name_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_type_from_molecule(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_type_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_name_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_index_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_id_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_type_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_name_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_index_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_id_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_type_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_index_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_id_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_name_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_type_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_index_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_id_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_name_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_type_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_atoms_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_atoms_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_groups_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_groups_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_components_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_components_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_molecules_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_molecules_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_chains_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_chains_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_entities_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_molecule (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonds_from_molecule as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

## chain

def get_index_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_id_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_name_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_type_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_index_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_id_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_id_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_name_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_name_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_type_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_type_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_index_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_index_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_id_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_id_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_name_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_name_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_type_from_chain(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_type_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_name_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_index_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_id_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_type_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_name_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_index_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_id_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_type_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_index_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_id_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_name_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_type_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_index_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_id_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_name_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_type_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_atoms_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_atoms_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_groups_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_groups_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_components_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_components_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_molecules_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_molecules_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_chains_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_chains_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_entities_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_chain (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonds_from_chain as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

## entity

def get_index_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_id_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_name_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_type_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_index_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_id_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_id_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_name_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_name_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_type_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_type_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_index_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_index_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_id_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_id_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_name_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_name_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_group_type_from_entity(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_group_type_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_name_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_index_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_id_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_component_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_component_type_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_name_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_index_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_id_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_chain_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_chain_type_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_index_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_id_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_name_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_molecule_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_molecule_type_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_index_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_id_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_name_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_entity_type_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_atoms_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_atoms_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_groups_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_groups_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_components_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_components_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_molecules_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_molecules_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_chains_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_chains_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_entities_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_entity (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonds_from_entity as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

## system

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonded_atoms_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_atoms_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_groups_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_components_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_chains_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_molecules_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_entities_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_aminoacids_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_aminoacids_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_nucleotides_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_nucleotides_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_ions_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_ions_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_waters_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_waters_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_cosolutes_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_cosolutes_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_small_molecules_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_small_molecules_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_peptides_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_peptides_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_proteins_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_proteins_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_dnas_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_dnas_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_rnas_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_rnas_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_lipids_from_system (item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_lipids_from_system as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_coordinates_from_system(item, indices='all', structure_indices='all'):

    tmp_item = item.xyz * 0.1 * unit.nanometers
    if structure_indices is not 'all':
        tmp_item = tmp_item[structure_indices,:,:]
    return tmp_item

def get_box_from_system(item, indices='all', structure_indices='all'):

    from molsysmt import box_vectors_from_box_lengths_and_angles
    lengths = get_box_lengths_from_system(item, indices=indices, structure_indices=structure_indices)
    angles = get_box_angles_from_system(item, indices=indices, structure_indices=structure_indices)
    tmp_item = box_vectors_from_box_lengths_and_angles(lengths, angles)
    return tmp_item

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    from molsysmt import box_shape_from_box_angles
    angles = get_box_angles_from_system(item, indices=indices, structure_indices=structure_indices)
    tmp_item = box_shape_from_box_angles(angles)
    return tmp_item

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    tmp_item = item.unitcells[:,0:3]*0.1*unit.nanometers
    if structure_indices is not 'all':
        tmp_item = tmp_item[structure_indices,:]
    return tmp_item

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    tmp_item = item.unitcells[:,3:6]*unit.degrees
    if structure_indices is not 'all':
        tmp_item = tmp_item[structure_indices,:]
    return tmp_item

def get_time_from_system(item, indices='all', structure_indices='all'):

    return item.time*unit.picoseconds

def get_step_from_system(item, indices='all', structure_indices='all'):

    return None

def get_frame_from_system(item, indices='all', structure_indices='all'):

    tmp_step = get_step_from_system(item, structure_indices=structure_indices)
    tmp_time = get_time_from_system(item, structure_indices=structure_indices)
    tmp_coordinates = get_coordinates_from_system(item, structure_indices=structure_indices)
    tmp_box = get_box_from_system(item, structure_indices=structure_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    return item.n_structures

def get_form_from_system(item, indices='all', structure_indices='all'):

    return form_name

## bond

def get_index_from_bond(item, indices='all', structure_indices='all'):

    return get_bond_index_from_bond(item, indices=indices)

def get_order_from_bond(item, indices='all', structure_indices='all'):

    return get_bond_order_from_bond(item, indices=indices)

def get_type_from_bond(item, indices='all', structure_indices='all'):

    return get_bond_type_from_bond(item, indices=indices)

def get_bond_index_from_bond(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_bond_index_from_bond as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_bond_order_from_bond as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_bond_type_from_bond as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_atom_index_from_bond as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

def get_n_bonds_from_bond(item, indices='all', structure_indices='all'):

    from .api_pytraj_Topology import get_n_bonds_from_bond as _get
    tmp_item = to_pytraj_Topology(item)
    return _get(tmp_item, indices=indices)

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotImplementedError

