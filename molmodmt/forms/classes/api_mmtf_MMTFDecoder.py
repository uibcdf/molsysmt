from os.path import basename as _basename
from mmtf import MMTFDecoder as _mmtf_MMTFDecoder

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mmtf_MMTFDecoder : form_name,
    'mmtf.MMTFDecoder' : form_name
}


def to_mmtf(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from mmtf.api.default_api import write_mmtf, MMTFDecoder
    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return write_mmtf(output_file_path, tmp_item, MMTFDecoder.pass_data_on)

def to_molmodmt_MolMod(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.io.molmod import from_mmtf_MMTFDecoder as mmtf_MMTFDecoder_to_molmodmt_MolMod
    return mmtf_MMTFDecoder_to_molmodmt_MolMod(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molmodmt_Composition(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.io.composition import from_mmtf_MMTFDecoder as mmtf_MMTFDecoder_to_molmodmt_Composition
    return mmtf_MMTFDecoder_to_molmodmt_Composition(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molmodmt_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.io.trajectory import from_mmtf_MMTFDecoder as mmtf_MMTFDecoder_to_molmodmt_Trajectory
    return mmtf_MMTFDecoder_to_molmodmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## atom

def get_frames_from_atom (item, indices='all', frame_indices='all'):

    from numpy import arange, empty, zeros, column_stack
    from molmodmt.utils.pbc import get_box_from_lengths_and_angles
    from molmodmt.utils import units as molmodmt_units
    from simtk.unit import angstroms, degrees, picoseconds

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')
    n_atoms = get_n_atoms_from_system(item, indices='all', frame_indices='all')

    step = arange(n_frames, dtype=int)
    time = zeros(n_frames, dtype=float)*picoseconds
    xyz = column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    xyz = xyz.reshape([-1, item.num_atoms, 3])
    xyz = xyz*angstroms

    cell_lengths = empty([n_frames,3], dtype='float64')
    cell_angles = empty([n_frames,3], dtype='float64')
    for ii in range(3):
        cell_lengths[:,ii] = item.unit_cell[ii]
        cell_angles[:,ii] = item.unit_cell[ii+3]

    cell_lengths = cell_lengths*angstroms
    cell_angles = cell_angles*degrees

    box = get_box_from_lengths_and_angles(cell_lengths, cell_angles)

    xyz = xyz.in_units_of(molmodmt_units.length)
    box = box.in_units_of(molmodmt_units.length)
    time = time.in_units_of(molmodmt_units.time)

    if frame_indices is not 'all':
        xyz = xyz[frame_indices,:,:]
        box = box[frame_indices,:,:]
        time = time[frame_indices]
        step = step[frame_indices]

    if indices is not 'all':
        xyz = xyz[:,indices,:]

    return step, time, xyz, box


## system

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.num_atoms

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return item.num_models

def get_frames_from_system (item, indices='all', frame_indices='all'):

    from numpy import arange, empty, zeros, column_stack
    from molmodmt.utils.pbc import get_box_from_lengths_and_angles
    from molmodmt.utils import units as molmodmt_units
    from simtk.unit import angstroms, degrees, picoseconds

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')
    n_atoms = get_n_atoms_from_system(item, indices='all', frame_indices='all')

    step = arange(n_frames, dtype=int)
    time = zeros(n_frames, dtype=float)*picoseconds
    xyz = column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    xyz = xyz.reshape([-1, item.num_atoms, 3])
    xyz = xyz*angstroms

    cell_lengths = empty([n_frames,3], dtype='float64')
    cell_angles = empty([n_frames,3], dtype='float64')
    for ii in range(3):
        cell_lengths[:,ii] = item.unit_cell[ii]
        cell_angles[:,ii] = item.unit_cell[ii+3]

    cell_lengths = cell_lengths*angstroms
    cell_angles = cell_angles*degrees

    box = get_box_from_lengths_and_angles(cell_lengths, cell_angles)

    xyz = xyz.in_units_of(molmodmt_units.length)
    box = box.in_units_of(molmodmt_units.length)
    time = time.in_units_of(molmodmt_units.time)

    if frame_indices is not 'all':
        xyz = xyz[frame_indices,:,:]
        box = box[frame_indices,:,:]
        time = time[frame_indices]
        step = step[frame_indices]

    return step, time, xyz, box

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

