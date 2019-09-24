from os.path import basename as _basename
from mdtraj.formats.hdf5 import HDF5TrajectoryFile as _mdtraj_HDF5TrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_HDF5TrajectoryFile: form_name,
    'mdtraj.HDF5TrajectoryFile': form_name
    }


#All of the data shall be n units of “nanometers”, “picoseconds”, “kelvin”, “degrees” and “kilojoules_per_mole”

def load_frame (item, indices=None, atom_indices=None):

    from molmodmt.utils.math import serie_to_chunks
    from molmodmt.utils.pbc import get_box_from_lengths_and_angles

    starts_serie_frames, size_serie_frames = serie_to_chunks(indices)

    xyz_list = []
    time_list = []
    step_list = []
    box_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        frame_hdf5 = item.read(n_frames=size, atom_indices=atom_indices)
        xyz = frame_hdf5.coordinates
        time = frame_hdf5.time
        cell_lengths = frame_hdf5.cell_lengths
        cell_angles = frame_hdf5.cell_angles
        box = get_box_from_lengths_and_angles(cell_lengths, cell_angles)
        xyz_list.append(xyz)
        time_list.append(time)
        box_list.append(box)

    xyz = _np.concatenate(xyz_list)
    del(xyz_list)
    time = _np.concatenate(time_list)
    del(time_list)
    step = indices
    box = _np.concatenate(box_list)
    del(box_list)

    xyz = xyz*_unit.nanometer
    box = box*_unit.nanometer
    time = time*_unit.picoseconds

    return step, time, xyz, box


#### Get

def get_frames_from_atom (item, indices=None, frame_indices=None):

    step, time, xyz, box = load_frame(item, frame_indices, indices)
    return step, time, xyz, box

# System

def get_frames_from_system (item, indices=None, frame_indices=None):

    step, time, xyz, box = load_frame(item, indices=frame_indices)
    return step, time, xyz, box

def get_n_frames_from_system (item, indices=None, frame_indices=None):

    return item._handle.root.coordinates.shape[0]

def get_box_shape_from_system (item, indices=None, frame_indices=None):

    from molmodmt.utils.pbc import get_shape_from_angles
    position = item.tell()
    frame_hdf5 = item.read(n_frames=1)
    cell_angles = frame_hdf5.cell_angles
    shape = get_shape_from_box(cell_angles)
    item.seek(position)
    del(frame_hdf5)
    return shape

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    return item.topology.n_atoms

