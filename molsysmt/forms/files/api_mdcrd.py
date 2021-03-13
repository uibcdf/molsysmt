from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='mdcrd'

is_form = {
    'mdcrd': form_name
    }

info=["",""]
with_topology=False
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False
with_simulation=False

info = ["AMBER mdcrd file format","https://ambermd.org/FileFormats.php#trajectory"]

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_mdcrd as mdcrd_to_molsysmt_MolSys

    tmp_item = mdcrd_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_mdcrd as mdcrd_to_molsysmt_Topology

    tmp_item = mdcrd_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_DataFrame(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_mdcrd as mdcrd_to_molsysmt_DataFrame

    tmp_item = mdcrd_to_molsysmt_DataFrame(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_mdcrd as mdcrd_to_molsysmt_Trajectory

    tmp_item = mdcrd_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def select_with_MDTraj(item, selection):

    return NotImplementedError

def select_with_MDTraj(item, selection):

    return NotImplementedError

def select_with_MolSysMT(item, selection):

    return NotImplementedError

def copy(item):

    return NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    return NotImplementedError

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

