from os.path import basename as _basename
from mdtraj.formats.pdb import PDBTrajectoryFile as _mdtraj_PDBTrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_PDBTrajectoryFile: form_name,
    'mdtraj.PDBTrajectoryFile': form_name
    }

def to_mdtraj_topology(item, atom_indices=None, frame_indices=None):

    from molmodmt import extract
    tmp_item = item.topology
    tmp_item = extract(tmp_item, selection=atom_indices)
    return tmp_item

def load_frame (item, indices=None, atom_indices=None):

    from numpy import array, concatenate, zeros, empty
    from molmodmt.utils.pbc import get_box_from_lengths_and_angles
    from molmodmt.utils import units as m3t_units
    from simtk.unit import angstroms, nanometers, degrees, picoseconds

    xyz_list = []
    time_list = []
    step_list = []
    box_list = []

    n_frames = len(indices)

    xyz = item.positions[indices,:,:]
    xyz = xyz[:,atom_indices,:]
    xyz = xyz*angstroms
    xyz = xyz.in_units_of(nanometers)

    time = zeros([len(indices)],dtype='int64')*picoseconds
    step = array(indices, dtype='int64')

    cell_lengths = empty([n_frames,3], dtype='float64')
    cell_angles = empty([n_frames,3], dtype='float64')
    for ii in range(3):
        cell_lengths[:,ii] = item.unitcell_lengths[ii]
        cell_angles[:,ii] = item.unitcell_angles[ii]

    cell_lengths = cell_lengths*angstroms
    cell_angles = cell_angles*degrees

    box = get_box_from_lengths_and_angles(cell_lengths*nanometers, cell_angles*degrees)

    xyz = xyz.astype('float64')
    box = box.astype('float64')
    time = time.astype('float64')
    step = step.astype('int64')

    xyz = xyz.in_units_of(m3t_units.length)
    box = box.in_units_of(m3t_units.length)
    time = time.in_units_of(m3t_units.time)

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

    return item.positions.shape[0]

def get_box_shape_from_system (item, indices=None, frame_indices=None):

    from molmodmt.utils.pbc import get_shape_from_angles
    from simtk.unit import degrees
    from numpy import empty

    cell_angles = empty([1,3], dtype='float64')
    for ii in range(3):
        cell_angles[0,ii] = item.unitcell_angles[ii]
    cell_angles = cell_angles*degrees
    shape = get_shape_from_angles(cell_angles)
    return shape

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    return item.topology.n_atoms

