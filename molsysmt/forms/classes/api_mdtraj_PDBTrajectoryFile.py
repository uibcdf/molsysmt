from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from mdtraj.formats.pdb import PDBTrajectoryFile as _mdtraj_PDBTrajectoryFile

form_name='mdtraj.PDBTrajectoryFile'

is_form={
    _mdtraj_PDBTrajectoryFile: form_name,
    }

info=["",""]
with_topology=True
with_coordinates=True
with_box=True
with_bonds=True
with_parameters=False

def to_mdtraj_topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from api_mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = item.topology
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def load_frame (item, atom_indices='all', frame_indices='all'):

    from molsysmt.pbc import box_vectors_from_box_lengths_and_angles
    from molsysmt._private_tools import units as molsysmt_units
    from simtk.unit import angstroms, nanometers, degrees, picoseconds
    from molsysmt._private_tools.atom_indices import digest as _digest_atom_indices
    from molsysmt._private_tools.frame_indices import digest as _digest_frame_indices

    atom_indices = _digest_atom_indices(item, atom_indices)
    frame_indices = _digest_frame_indices(item, frame_indices)

    xyz_list = []
    time_list = []
    step_list = []
    box_list = []

    n_frames = len(frame_indices)

    xyz = item.positions[frame_indices,:,:]
    xyz = xyz.astype('float64')
    xyz = xyz[:,atom_indices,:]
    xyz = xyz*angstroms
    xyz = xyz.in_units_of(nanometers)

    #time = zeros([len(frame_indices)],dtype='float64')*picoseconds
    #step = array(frame_indices, dtype='int64')

    time = np.array([None for ii in range(n_frames)])*picoseconds
    step = np.array([None for ii in range(n_frames)])

    if item.unitcell_lengths is not None:

        cell_lengths = np.empty([n_frames,3], dtype='float64')
        cell_angles = np.empty([n_frames,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unitcell_lengths[ii]
            cell_angles[:,ii] = item.unitcell_angles[ii]

        cell_lengths = cell_lengths*angstroms
        cell_angles = cell_angles*degrees

        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        box = box.in_units_of(molsysmt_units.length)

    else:

        box = None

    xyz = xyz.in_units_of(molsysmt_units.length)
    time = time.in_units_of(molsysmt_units.time)

    return step, time, xyz, box

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

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

#### Get

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_index_from_atom as _get
    return _get(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

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

    from molsysmt.elements.molecule import get_molecule_type_from_molecule as get
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

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.topology.n_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_n_components_from_system as get
    return get(item, indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_n_molecules_from_system as get
    return get(item, indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_n_entities_from_system as get
    return get(item, indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    from molsysmt._private_tools.pbc import get_shape_from_angles
    from simtk.unit import degrees
    from numpy import empty

    cell_angles = empty([1,3], dtype='float64')
    for ii in range(3):
        cell_angles[0,ii] = item.unitcell_angles[ii]
    cell_angles = cell_angles*degrees
    shape = get_shape_from_angles(cell_angles)
    return shape

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

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return item.positions.shape[0]

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_box:
        tmp_box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
        if tmp_box[0] is not None:
            output = True

    return output

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_topology:
        if get_n_bonds_from_system(item, indices=indices, frame_indices=frame_indices):
            output = True

    return output

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

