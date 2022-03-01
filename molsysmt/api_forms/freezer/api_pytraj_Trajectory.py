from molsysmt._private_tools.exceptions import *
from molsysmt.api_forms.common_gets import *
import numpy as np
from pytraj import Trajectory as _pytraj_Trajectory
from molsysmt.native.molecular_system import molecular_system_components

form_name='pytraj.Trajectory'
from_type='class'

is_form={
    _pytraj_Trajectory : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_pytraj_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_pytraj_Topology import to_pytraj_Topology as pytraj_Topology_to_pytraj_Topology

    tmp_item = item.topology
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = pytraj_Topology_to_pytraj_Topology(tmp_item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.molsys import from_pytraj_Trajectory as pytraj_Topology_to_molsysmt_MolSys
    from molsysmt.api_forms.api_molsysmt_MolSys import to_molsysmt_MolSys as molsysmt_MolSys_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = pytraj_Topology_to_molsysmt_MolSys(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_molsysmt_MolSys(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.topology import from_pytraj_Trajectory as pytraj_Trajectory_to_molsysmt_Topology
    from molsysmt.api_forms.api_molsysmt_Topology import to_molsysmt_Topology as molsysmt_Topology_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = pytraj_Trajectory_to_molsysmt_Topology(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = molsysmt_Topology_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.trajectory import from_pytraj_Trajectory as pytraj_Trajectory_to_molsysmt_Trajectory
    from molsysmt.api_forms.api_molsysmt_Trajectory import to_molsysmt_Trajectory as molsysmt_Trajectory_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = pytraj_Trajectory_to_molsysmt_Trajectory(item,
            molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = molsysmt_Trajectory_to_molsysmt_Trajectory(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_pytraj_Trajectory(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        raise NotImplementedError()
    else:
        raise NotImplementedError()

def extract(item, atom_indices='all', structure_indices='all'):

    raise NotImplementedError()

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

def get_n_frames_from_atom(item, indices='all', structure_indices='all'):

    return get_n_frames_from_system(item, indices='all', structure_indices='all')

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

def get_n_frames_from_system(item, indices='all', structure_indices='all'):

    return item.n_frames

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

