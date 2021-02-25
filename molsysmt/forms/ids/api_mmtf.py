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
with_trajectory=True
with_coordinates=True
with_box=True
with_bonds=True
with_parameters=False

def to_mmtf(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from mmtf import fetch
    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_mmtf as MMTFDecoder_to_mmtf

    tmp_item = to_mmtf_MMTFDecoder(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = MMTFDecoder_to_mmtf(tmp_item, output_filename=output_filename)

    return tmp_item

def to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mmtf import fetch
    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import extract as extract_MMTFDecoder

    tmp_item = item.split(':')[-1]
    tmp_item = fetch(tmp_item)
    tmp_item = extract_MMTFDecoder(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.ids import from_mmtf as mmtf_to_molsysmt_MolSys

    tmp_item = mmtf_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.ids import from_mmtf as mmtf_to_molsysmt_Topology

    tmp_item = mmtf_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_DataFrame(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.ids import from_mmtf as mmtf_to_molsysmt_DataFrame

    tmp_item = mmtf_to_molsysmt_DataFrame(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.ids import from_mmtf as mmtf_to_molsysmt_Trajectory

    tmp_item = mmtf_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_Trajectory as mmtf_MMTFDecoder_to_molsysmt_Trajectory

    tmp_item = to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def view_with_NGLView(item, atom_indices='all', frame_indices='all'):

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

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    tmp_item = to_mmtf_MMTFDecoder(item)
    return tmp_item.num_atoms

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    tmp_item = to_mmtf_MMTFDecoder(item)
    return tmp_item.num_models

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

