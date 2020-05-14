from os.path import basename as _basename
from molsysmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'xtc': form_name
    }

info=["",""]
with_topology=False
with_trajectory=True

def to_molsysmt_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_xtc
    return from_xtc(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_mdtraj_XTCTrajectoryFile(item, atom_indices='all', frame_indices='all'):

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

