from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
from molsysmt import puw
import numpy as np
from mmtf import MMTFDecoder as _mmtf_MMTFDecoder
from molsysmt.native.molecular_system import molecular_system_components
import importlib
import sys

form_name='mmtf.MMTFDecoder'

is_form={
    _mmtf_MMTFDecoder : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_file_mmtf(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    tmp_item, tmp_molecular_system = to_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)
    tmp_item = output_filename
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.api_molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_file_pdb(tmp_item, molecular_system=tmp_molecular_system, output_filename=output_filename)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys import from_mmtf_MMTFDecoder as molsysmt_MolSys_from_mmtf_MMTFDecoder

    tmp_item, tmp_molecular_system = molsysmt_MolSys_from_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology import from_mmtf_MMTFDecoder as molsysmt_Topology_from_mmtf_MMTFDecoder

    tmp_item, tmp_molecular_system = molsysmt_Topology_from_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory import from_mmtf_MMTFDecoder as molsysmt_Trajectory_from_mmtf_MMTFDecoder

    tmp_item, tmp_molecular_system = molsysmt_Trajectory_from_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_mdtraj_Trajectory(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_mmtf_MMTFDecoder(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def aux_get(item, indices='all', frame_indices='all'):

    tmp_item, _ = to_molsysmt_Topology(item)
    method_name = sys._getframe(1).f_code.co_name
    module = importlib.import_module('molsysmt.forms.api_molsysmt_Topology')
    _get = getattr(module, method_name)
    output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    return output

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

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

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.num_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.num_groups

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

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

    raise NotImplementedError()

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError()

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError()

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError()

def get_time_from_system(item, indices='all', frame_indices='all'):

    return None

def get_step_from_system(item, indices='all', frame_indices='all'):

    return None

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return item.num_models

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError()

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError()

