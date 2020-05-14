import numpy as np
from simtk import unit
from os.path import basename
from mdtraj.formats import GroTrajectoryFile as _mdtraj_GroTrajectoryFile

form_name=basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_GroTrajectoryFile: form_name,
    'mdtraj.GroTrajectoryFile': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True

def load_frame (item, atom_indices='all', frame_indices='all'):

    # It doesn't really work. seek doesn't work. Once the file is read can not be rewinded.

    step = None

    if frame_indices is 'all':

        coordinates, time, box = item.read()

        if atom_indices is not 'all':

            coordinates = coordinates[:,atom_indices,:]

        print(step, time, coordinates, box)

    else:

        from molsysmt.utils.math import serie_to_chunks

        starts_serie_frames, size_serie_frames = serie_to_chunks(frame_indices)

        coordinates_list = []
        time_list = []
        step_list = []
        box_list = []

        for start, size in zip(starts_serie_frames, size_serie_frames):
            item.seek(start)
            coordinates, time, box = item.read(n_frames=size, atom_indices=atom_indices)
            coordinates_list.append(coordinates)
            time_list.append(time)
            step_list.append(step)
            box_list.append(box)

        coordinates = np.concatenate(coordinates_list)
        time = np.concatenate(time_list)
        box = np.concatenate(box_list)
        del(coordinates_list, time_list, box_list)

    if len(box)==0:
        box = None
    else:
        box = box*unit.nanometer
    if len(time)==0:
        time = None
    else:
        time = time*unit.picoseconds
    coordinates = coordinates*unit.nanometer


    return step, time, coordinates, box

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

#### Get

# atom

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system(item)
    else:
        return len(indices)

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    step, time, coordinates, box = load_frame(item, atom_indices=indices, frame_indices=frame_indices)
    return step, time, coordinates, box


# system

def get_frame_from_system (item, indices='all', frame_indices='all'):

    step, time, coordinates, box = load_frame(item, frame_indices=frame_indices)
    return step, time, coordinates, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    _, _, box = item.read()
    n_frames = box.shape[0]
    del(box)
    return n_frames

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

