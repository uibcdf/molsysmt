from molsysmt._private_tools.exceptions import *
from molsysmt.tools.mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology

from molsysmt import puw
import numpy as np
import importlib
import sys

###### Get

def aux_get(item, indices='all', frame_indices='all'):

    tmp_item, _ = to_molsysmt_Topology(item, check_form=False)
    method_name = sys._getframe(1).f_code.co_name
    module = importlib.import_module('molsysmt.tools.molsysmt_Topology')
    _get = getattr(module, method_name)
    output = _get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

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

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return item.num_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return item.num_groups

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return item.num_bonds

def get_box_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

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

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    raise NotImplementedError()

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    raise NotImplementedError()

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    raise NotImplementedError()

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    raise NotImplementedError()

def get_time_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return None

def get_step_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return None

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return item.num_models

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return form_name

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    return aux_get(item, indices=indices, frame_indices=frame_indices)

