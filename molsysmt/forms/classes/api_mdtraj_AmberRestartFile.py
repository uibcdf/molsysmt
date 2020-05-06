from os.path import basename as _basename
from mdtraj.formats import AmberRestartFile as _mdtraj_AmberRestartFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_AmberRestartFile: form_name,
    'mdtraj.AmberRestartFile': form_name
    }

info=["",""]
with_topology=False
with_trajectory=True

def load_frame (item, atom_indices='all', frame_indices='all'):

    from molsysmt.pbc import box_vectors_from_box_lengths_and_angles
    from molsysmt.utils import units as molsysmt_units
    from simtk.unit import angstroms, nanometers, degrees, picoseconds
    from molsysmt.utils.atom_indices import digest as _digest_atom_indices
    from molsysmt.utils.frame_indices import digest as _digest_frame_indices

    atom_indices = _digest_atom_indices(item, atom_indices)
    frame_indices = _digest_frame_indices(item, frame_indices)

    xyz, time, cell_lengths, cell_angles = item.read()

    xyz = item.positions[frame_indices,:,:]
    xyz = xyz[:,atom_indices,:]
    xyz = xyz*angstroms

    time = time[frame_indices]*picoseconds
    step = None

    if item.unitcell_lengths is not None:

        cell_lengths = cell_lengths*angstroms
        cell_angles = cell_angles*degrees
        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        box = box[frame_indices,:,:]
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

    return get_frame_from_atom(item, indices='all', frame_indices=frame_indices)

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return item.n_frames

def get_box_shape_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_shape_from_box_angles
    from simtk.unit import degrees
    from numpy import empty

    _, _, _, cell_angles = item.read()
    cell_angles = cell_angles*degrees
    shape = get_shape_from_angles(cell_angles)
    return shape

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    xyz, _, _, _ = item.read()

    return xyz.shape[1]

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

