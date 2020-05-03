from os.path import basename as _basename
from mmtf import MMTFDecoder as _mmtf_MMTFDecoder

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mmtf_MMTFDecoder : form_name,
    'mmtf.MMTFDecoder' : form_name
}

info=["",""]

def to_mmtf(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from mmtf.api.default_api import write_mmtf, MMTFDecoder
    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return write_mmtf(output_file_path, tmp_item, MMTFDecoder.pass_data_on)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_mmtf_MMTFDecoder as molsysmt_MolSys_from_mmtf_MMTFDecoder
    return molsysmt_MolSys_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Composition(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.composition.classes import from_mmtf_MMTFDecoder as molsysmt_Composition_from_mmtf_MMTFDecoder
    return molsysmt_Composition_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.classes import from_mmtf_MMTFDecoder as molsysmt_Composition_from_mmtf_MMTFDecoder
    return molsysmt_Composition_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_mmtf_MMTFDecoder as molsysmt_Trajectory_from_mmtf_MMTFDecoder
    return molsysmt_Trajectory_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_DataFrame import select_with_MolSysMT as select_DataFrame_with_MolSysMT
    tmp_item = to_molsysmt_DataFrame(item)
    return select_DataFrame_with_MolSysMT(tmp_item, selection)

###### Get

## atom

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    from numpy import arange, empty, zeros, column_stack
    from molsysmt import box_vectors_from_box_lengths_and_angles
    from molsysmt.utils import units as molsysmt_units
    from simtk.unit import angstroms, degrees, picoseconds

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')
    n_atoms = get_n_atoms_from_system(item, indices='all', frame_indices='all')

    step = arange(n_frames, dtype=int)
    time = zeros(n_frames, dtype=float)*picoseconds
    xyz = column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    xyz = xyz.reshape([-1, item.num_atoms, 3])
    xyz = xyz*angstroms

    if item.unit_cell is not None:

        cell_lengths = empty([n_frames,3], dtype='float64')
        cell_angles = empty([n_frames,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = cell_lengths*angstroms
        cell_angles = cell_angles*degrees

        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        box = box.in_units_of(molsysmt_units.length)

    else:

        box = None

    xyz = xyz.in_units_of(molsysmt_units.length)
    time = time.in_units_of(molsysmt_units.time)

    if frame_indices is not 'all':
        xyz = xyz[frame_indices,:,:]
        time = time[frame_indices]
        step = step[frame_indices]
        if box is not None:
            box = box[frame_indices,:,:]

    if indices is not 'all':
        xyz = xyz[:,indices,:]

    return step, time, xyz, box


## system

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return item.num_atoms

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return item.num_models

def get_frame_from_system (item, indices='all', frame_indices='all'):

    return get_frame_from_atom (item, indices='all', frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

