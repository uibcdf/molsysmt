from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
from molsysmt import puw
import numpy as np
from mmtf import MMTFDecoder as _mmtf_MMTFDecoder
from molsysmt.molecular_system import molecular_system_components

form_name='mmtf.MMTFDecoder'

is_form={
    _mmtf_MMTFDecoder : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_mmtf(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)

    return output_filename

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_mmtf_MMTFDecoder as molsysmt_MolSys_from_mmtf_MMTFDecoder

    tmp_item = molsysmt_MolSys_from_mmtf_MMTFDecoder(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_mmtf_MMTFDecoder as molsysmt_Topology_from_mmtf_MMTFDecoder

    tmp_item = molsysmt_Topology_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_mmtf_MMTFDecoder as molsysmt_Trajectory_from_mmtf_MMTFDecoder

    tmp_item = molsysmt_Trajectory_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def select_with_Amber(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select_Topology_with_MolSysMT
    tmp_item = to_molsysmt_Topology(item)
    return select_Topology_with_MolSysMT(tmp_item, selection)

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

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')
    n_atoms = get_n_atoms_from_system(item, indices='all', frame_indices='all')

    xyz = np.column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    xyz = xyz.reshape([-1, item.num_atoms, 3])
    xyz = puw.quantity(xyz, 'angstroms')
    xyz = puw.standardize(xyz)

    if frame_indices is not 'all':
        xyz = xyz[frame_indices,:,:]

    if indices is not 'all':
        xyz = xyz[:,indices,:]

    return xyz

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

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

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.num_atoms

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

    return item.num_bonds

def get_box_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_vectors_from_box_lengths_and_angles

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')

    if item.unit_cell is not None:

        cell_lengths = np.empty([n_frames,3], dtype='float64')
        cell_angles = np.empty([n_frames,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        box = puw.standardize(box)

    else:

        box = None

    if frame_indices is not 'all':
        if box is not None:
            box = box[frame_indices,:,:]

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

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')

    time = puw.quantity(np.zeros(n_frames, dtype=float), 'picoseconds')
    time = puw.standardize(time)

    if frame_indices is not 'all':
        time = time[frame_indices]

    return time

def get_step_from_system(item, indices='all', frame_indices='all'):

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')

    step = np.arange(n_frames, dtype=int)

    if frame_indices is not 'all':
        step = step[frame_indices]

    return step

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return item.num_models

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

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

