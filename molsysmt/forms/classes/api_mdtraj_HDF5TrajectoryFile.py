from os.path import basename as _basename
from mdtraj.formats.hdf5 import HDF5TrajectoryFile as _mdtraj_HDF5TrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_HDF5TrajectoryFile: form_name,
    'mdtraj.HDF5TrajectoryFile': form_name
    }

info=["",""]

def load_frame (item, atom_indices='all', frame_indices='all'):

    #All of the data shall be n units of “nanometers”, “picoseconds”, “kelvin”, “degrees” and “kilojoules_per_mole”

    from numpy import array, concatenate
    from molsysmt.utils.math import serie_to_chunks
    from molsysmt.utils.pbc import get_box_from_lengths_and_angles
    from simtk.unit import nanometers, picoseconds, degrees

    starts_serie_frames, size_serie_frames = serie_to_chunks(indices)

    xyz_list = []
    time_list = []
    step_list = []
    box_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        frame_hdf5 = item.read(n_frames=size, atom_indices=atom_indices)
        xyz = frame_hdf5.coordinates
        xyz_list.append(xyz)
        time = frame_hdf5.time
        time_list.append(time)
        cell_lengths = frame_hdf5.cell_lengths
        cell_angles = frame_hdf5.cell_angles
        box = get_box_from_lengths_and_angles(cell_lengths*nanometers, cell_angles*degrees)
        box_list.append(box._value)

    step = array([],dtype=int)
    xyz = concatenate(xyz_list)
    del(xyz_list)
    time = concatenate(time_list)
    del(time_list)
    box = concatenate(box_list)
    del(box_list)

    xyz = xyz.astype('float64')
    box = box.astype('float64')
    time = time.astype('float64')
    step = step.astype('int64')

    xyz = xyz*nanometers
    box = box*nanometers
    time = time*picoseconds

    return step, time, xyz, box

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

#### Get

# atom

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    step, time, xyz, box = load_frame(item, atom_indices=indices, frame_indices=frame_indices)
    return step, time, xyz, box

# system

def get_frame_from_system (item, indices='all', frame_indices='all'):

    step, time, xyz, box = load_frame(item, frame_indices=frame_indices)
    return step, time, xyz, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return item._handle.root.coordinates.shape[0]

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.utils.pbc import get_shape_from_angles
    position = item.tell()
    frame_hdf5 = item.read(n_frames=1)
    cell_angles = frame_hdf5.cell_angles
    shape = get_shape_from_angles(cell_angles)
    item.seek(position)
    del(frame_hdf5)
    return shape

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.topology.n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

