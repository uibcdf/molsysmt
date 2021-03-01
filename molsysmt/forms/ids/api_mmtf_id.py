from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
import urllib
import json

form_name='mmtf:id'

is_form = {
    'mmtf:id': form_name,
    'MMTF:id': form_name
    }

info=["",""]
with_topology=True
with_coordinates=True
with_box=True
with_bonds=True
with_parameters=False

def to_mmtf(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from mmtf import fetch
    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_mmtf as MMTFDecoder_to_mmtf

    tmp_item = to_mmtf_MMTFDecoder(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = MMTFDecoder_to_mmtf(tmp_item, output_filename=output_filename)

    return tmp_item

def to_mmtf_MMTFDecoder(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mmtf import fetch
    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import extract as extract_MMTFDecoder

    tmp_item = item.split(':')[-1]
    tmp_item = fetch(tmp_item)
    tmp_item = extract_MMTFDecoder(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.ids import from_mmtf_id as mmtf_id_to_molsysmt_MolSys

    tmp_item = mmtf_id_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.ids import from_mmtf_id as mmtf_id_to_molsysmt_Topology

    tmp_item = mmtf_id_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_DataFrame(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.ids import from_mmtf_id as mmtf_id_to_molsysmt_DataFrame

    tmp_item = mmtf_id_to_molsysmt_DataFrame(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.ids import from_mmtf_id as mmtf_id_to_molsysmt_Trajectory

    tmp_item = mmtf_id_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_Trajectory as mmtf_MMTFDecoder_to_molsysmt_Trajectory

    tmp_item = to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def view_with_NGLView(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

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

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

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

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

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

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

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

    return with_box

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    return with_bonds

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


## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    tmp_item = to_mmtf_MMTFDecoder(item)
    return tmp_item.num_atoms

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    tmp_item = to_mmtf_MMTFDecoder(item)
    return tmp_item.num_models

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

