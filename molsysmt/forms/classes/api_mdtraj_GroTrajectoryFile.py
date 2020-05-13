import numpy as _np
from simtk import unit as _unit
from os.path import basename as _basename
from mdtraj.formats import GroTrajectoryFile as _mdtraj_GroTrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_GroTrajectoryFile: form_name,
    'mdtraj.GroTrajectoryFile': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True

def load_frame (item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

#### Get

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    step, time, xyz, box = load_frame(item, atom_indices=indices, frame_indices=frame_indices)
    return step, time, xyz, box

# system

def get_frame_from_system (item, indices='all', frame_indices='all'):

    step, time, xyz, box = load_frame(item, frame_indices=frame_indices)
    return step, time, xyz, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

