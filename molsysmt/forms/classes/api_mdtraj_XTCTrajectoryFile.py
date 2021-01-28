import numpy as _np
from simtk import unit as _unit
from os.path import basename as _basename
from mdtraj.formats.xtc import XTCTrajectoryFile as _mdtraj_XTCTrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_XTCTrajectoryFile: form_name,
    'mdtraj.XTCTrajectoryFile': form_name
    }

info=["",""]
with_topology=False
with_coordinates=True
with_box=True
with_parameters=False

def load_frame (item, atom_indices='all', frame_indices='all',
    topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    if frame_indices is 'all':

        n_frames= get_n_frames_from_system(item)
        frame_indices = _np.arange(n_frames)

    from molsysmt._private_tools.math import serie_to_chunks

    starts_serie_frames, size_serie_frames = serie_to_chunks(frame_indices)

    xyz_list = []
    time_list = []
    step_list = []
    box_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        if atom_indices is 'all':
            xyz, time, step, box = item.read(n_frames=size)
        else:
            xyz, time, step, box = item.read(n_frames=size, atom_indices=atom_indices)
        xyz_list.append(xyz)
        time_list.append(time)
        step_list.append(step)
        box_list.append(box)

    xyz = _np.concatenate(xyz_list)
    del(xyz_list)
    time = _np.concatenate(time_list)
    del(time_list)
    step = _np.concatenate(step_list)
    del(step_list)
    box = _np.concatenate(box_list)
    del(box_list)

    xyz = xyz.astype('float64')
    box = box.astype('float64')
    time = time.astype('float64')
    step = step.astype('int64')

    xyz = xyz*_unit.nanometer
    box = box*_unit.nanometer
    time = time*_unit.picoseconds

    return step, time, xyz, box

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

    return len(item.offsets)

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    from molsysmt._private_tools.pbc import get_shape_from_box
    position = item.tell()
    xyz, time, step, box = item.read(n_frames=1)
    item.seek(position)
    shape = get_shape_from_box(box*_unit.nanometers)
    del(xyz, time, step, box)
    return shape

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    position = item.tell()
    xyz, time, step, box = item.read(n_frames=1)
    n_atoms = xyz.shape[1]
    del(xyz, time, step, box)
    item.seek(position)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import get_form
    return get_form(item)

