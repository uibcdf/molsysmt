import numpy as np
from molsysmt.forms.common_gets import *
from molsysmt._private_tools.exceptions import *
from molsysmt import puw

form_name='mmtf'

is_form = {
    'mmtf': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True
with_coordinates=True
with_box=True
with_bonds=True
with_parameters=False

def to_mmtf_MMTFDecoder(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mmtf import parse
    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder

    tmp_item = parse(item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices='all', frame_indices='all')

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys

    tmp_item = to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology

    tmp_item = to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_Trajectory as mmtf_MMTFDecoder_to_molsysmt_Trajectory

    tmp_item = to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_aminoacids1_seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import to_aminoacids1_seq as molsysmt_Topology_to_aminoacids1_seq

    tmp_item = to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_Topology_to_aminoacids1_seq(tmp_item)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis import Universe
    from molsysmt.forms.classes.api_mdanalysis_Universe import extract as extract_mdanalysis_Universe

    tmp_item = Universe(item)
    tmp_item = extract_mdanalysis_Universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import select_with_MDTraj as select_mmtf_MMTFDecoder_with_MDTraj
    tmp_item = to_mmtf_MMTFDecoder(item)
    return select_mmtf_MMTFDecoder_with_MDTraj(tmp_item, selection)

def select_with_MolSysMT(item, selection):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import select_with_MolSysMT as select_mmtf_MMTFDecoder_with_MolSysMT
    tmp_item = to_mmtf_MMTFDecoder(item)
    return select_mmtf_MMTFDecoder_with_MolSysMT(tmp_item, selection)

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

def view_with_NGLView(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError


##### Get

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):


    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_atom_id_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_atom_name_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_atom_type_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_group_index_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_component_index_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_chain_index_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_molecule_index_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_entity_index_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_inner_bonded_atoms_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_inner_bonded_bonds_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_coordinates_from_atom as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_group_id_from_group as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_group_name_from_group as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_group_type_from_group as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_component_id_from_component as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_component_name_from_component as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_component_type_from_component as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_molecule_id_from_molecule as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_molecule_name_from_molecule as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_molecule_type_from_molecule as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_chain_id_from_chain as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_chain_name_from_chain as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_chain_type_from_chain as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_entity_id_from_entity as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_entity_name_from_entity as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_entity_type_from_entity as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

# System

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_n_atoms_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_n_groups_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_n_components_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_n_chains_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_n_molecules_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_n_entities_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_n_bonds_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_coordinates_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_box_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_box_shape_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_box_lengths_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_box_angles_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_box_volume_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_time_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_step_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_step_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_step_from_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import get_bonded_atoms_system as _get
    tmp_item = to_mmtf_MMTFDecoder(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

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

    if with_bonds:
        if get_n_bonds_from_system(item, indices=indices, frame_indices=frame_indices):
            output = True

    return output


###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

