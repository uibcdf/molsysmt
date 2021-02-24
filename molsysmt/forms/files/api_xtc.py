from os.path import basename as _basename
from molsysmt._private_tools.exceptions import *
import simtk.unit as unit
from molsysmt.forms.common_gets import *
import numpy as np

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'xtc': form_name
    }

info=["",""]
with_topology=False
with_coordinates=True
with_box=True
with_parameters=False

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all',
                           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.files import from_xtc
    return from_xtc(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_mdtraj_XTCTrajectoryFile(item, atom_indices='all', frame_indices='all',
                                topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from mdtraj.formats import XTCTrajectoryFile
    return XTCTrajectoryFile(item)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

#### Get

def get_frames_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='atom', indices=indices,
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system (item)
    else:
        return len(indices)

def get_n_frames_from_atom (item, indices='all', frame_indices='all'):

    return get_n_frames_from_system(item, frame_indices=frame_indices)

# System

def get_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='system',
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    n_frames = get(tmp_item, target='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    n_atoms = get(tmp_item, target='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

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

