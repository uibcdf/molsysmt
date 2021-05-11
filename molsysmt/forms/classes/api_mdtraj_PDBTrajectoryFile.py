from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from mdtraj.formats.pdb import PDBTrajectoryFile as _mdtraj_PDBTrajectoryFile
import importlib
import sys
from molsysmt import puw
from molsysmt.molecular_system import molecular_system_components

form_name='mdtraj.PDBTrajectoryFile'

is_form={
    _mdtraj_PDBTrajectoryFile: form_name,
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_mdtraj_Topology as mdtraj_Topology_to_mdtraj_Topology

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_mdtraj_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def select_with_Amber(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def to_mdtraj_PDBTrajectoryFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

#### Get

def aux_get(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    if 'mdtraj.Topology' in forms:

        tmp_item = to_mdtraj_Topology(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    else:

        raise NotImplementedError

    return output

## atom

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

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

    xyz = item.positions

    if frame_indices is not 'all':
        xyz = xyz[frame_indices,:,:]
    if indices is not 'all':
        xyz = xyz[:,indices,:]

    xyz = xyz*puw.unit(item.distance_unit)
    xyz = puw.standardize(xyz)

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

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_vectors_from_box_lengths_and_angles

    cell_lengths = item.unitcell_lengths
    cell_angles = item.unitcell_angles

    if cell_lengths is not None:

        cell_lengths = cell_lengths*puw.unit(item.distance_unit)
        cell_angles = cell_angles*puw.unit('degrees')
        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        if frame_indices is not 'all':
            box = box[frame_indices,:,:]
        box = puw.standardize(box)

    else:

        box = None

    return box

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    cell_lengths = item.unitcell_lengths

    if cell_lengths is not None:

        cell_lengths = cell_lengths*puw.unit(item.distance_unit)
        if frame_indices is not 'all':
            cell_lengths = cell_lengths[frame_indices]
        cell_lengths = puw.standardize(cell_lengths)

    else:

        cell_lengths = None

    return cell_lengths

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    cell_angles = item.unitcell_angles

    if cell_lengths is not None:

        cell_angles = cell_angles*puw.unit('degrees')
        if frame_indices is not 'all':
            cell_angles = cell_angles[frame_indices]
        cell_angles = puw.standardize(cell_angles)

    else:

        cell_angles = None

    return cell_angles

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    return None

def get_step_from_system(item, indices='all', frame_indices='all'):

    return None

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return item.positions.shape[0]

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

