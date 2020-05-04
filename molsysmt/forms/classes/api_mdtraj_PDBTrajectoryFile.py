from os.path import basename as _basename
from mdtraj.formats.pdb import PDBTrajectoryFile as _mdtraj_PDBTrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_PDBTrajectoryFile: form_name,
    'mdtraj.PDBTrajectoryFile': form_name
    }

info=["",""]

def to_mdtraj_topology(item, atom_indices='all', frame_indices='all'):

    from api_mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = item.topology
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def load_frame (item, atom_indices='all', frame_indices='all'):

    from numpy import array, concatenate, zeros, empty, full
    from molsysmt.pbc import box_vectors_from_box_lengths_and_angles
    from molsysmt.utils import units as molsysmt_units
    from simtk.unit import angstroms, nanometers, degrees, picoseconds
    from molsysmt.utils.atom_indices import digest as _digest_atom_indices
    from molsysmt.utils.frame_indices import digest as _digest_frame_indices

    atom_indices = _digest_atom_indices(item, atom_indices)
    frame_indices = _digest_frame_indices(item, frame_indices)

    xyz_list = []
    time_list = []
    step_list = []
    box_list = []

    n_frames = len(frame_indices)

    xyz = item.positions[frame_indices,:,:]
    xyz = xyz.astype('float64')
    xyz = xyz[:,atom_indices,:]
    xyz = xyz*angstroms
    xyz = xyz.in_units_of(nanometers)

    time = zeros([len(frame_indices)],dtype='float64')*picoseconds
    step = array(frame_indices, dtype='int64')

    if item.unitcell_lengths is not None:

        cell_lengths = empty([n_frames,3], dtype='float64')
        cell_angles = empty([n_frames,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unitcell_lengths[ii]
            cell_angles[:,ii] = item.unitcell_angles[ii]

        cell_lengths = cell_lengths*angstroms
        cell_angles = cell_angles*degrees

        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        box = box.in_units_of(molsysmt_units.length)

    else:

        box = None

    xyz = xyz.in_units_of(molsysmt_units.length)
    time = time.in_units_of(molsysmt_units.time)

    return step, time, xyz, box

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

#### Get

# atom

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    step, time, xyz, box = load_frame(item, atom_indices=indices, frame_indices=frame_indices)
    return step, time, xyz, box

# system

def get_frame_from_system (item, indices='all', frame_indices='all'):

    step, time, xyz, box = load_frame(item, atom_indices='all', frame_indices=frame_indices)
    return step, time, xyz, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return item.positions.shape[0]

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.utils.pbc import get_shape_from_angles
    from simtk.unit import degrees
    from numpy import empty

    cell_angles = empty([1,3], dtype='float64')
    for ii in range(3):
        cell_angles[0,ii] = item.unitcell_angles[ii]
    cell_angles = cell_angles*degrees
    shape = get_shape_from_angles(cell_angles)
    return shape

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.topology.n_atoms

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    step, time, xyz, box = load_frame(item, atom_indices=indices, frame_indices=frame_indices)
    return step, time, xyz, box

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

