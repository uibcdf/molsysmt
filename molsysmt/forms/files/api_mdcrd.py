from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='mdcrd'

is_form = {
    'mdcrd': form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates', 'box']:
    has[ii]=True

info = ["AMBER mdcrd file format","https://ambermd.org/FileFormats.php#trajectory"]

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_mdcrd as mdcrd_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = mdcrd_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_mdcrd as mdcrd_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = mdcrd_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_DataFrame(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_mdcrd as mdcrd_to_molsysmt_DataFrame

    tmp_item, tmp_molecular_system = mdcrd_to_molsysmt_DataFrame(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_mdcrd as mdcrd_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = mdcrd_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def select_with_MDTraj(item, selection):

    return NotImplementedError

def select_with_MDTraj(item, selection):

    return NotImplementedError

def select_with_MolSysMT(item, selection):

    return NotImplementedError

def to_mdcrd(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None, copy_if_all=True):

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


def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

# System

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return NotImplementedError

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return NotImplementedError

