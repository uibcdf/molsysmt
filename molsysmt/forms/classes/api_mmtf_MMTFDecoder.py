from os.path import basename as _basename
from mmtf import MMTFDecoder as _mmtf_MMTFDecoder

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mmtf_MMTFDecoder : form_name,
    'mmtf.MMTFDecoder' : form_name
}

info=["",""]
with_topology=True
with_coordinates=True
with_box=True
with_parameters=False

def to_mmtf(item, atom_indices='all', frame_indices='all', output_filename=None,
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from mmtf.api.default_api import write_mmtf, MMTFDecoder
    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.classes import from_mmtf_MMTFDecoder as molsysmt_MolSys_from_mmtf_MMTFDecoder
    return molsysmt_MolSys_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.classes import from_mmtf_MMTFDecoder as molsysmt_Topology_from_mmtf_MMTFDecoder
    return molsysmt_Topology_from_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

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

    from .api_molsysmt_Topology import select_with_MolSysMT as select_Topology_with_MolSysMT
    tmp_item = to_molsysmt_Topology(item)
    return select_Topology_with_MolSysMT(tmp_item, selection)

###### Get

## atom

def get_frame_from_atom (item, indices='all', frame_indices='all'):

    import pyunitwizard as puw
    from molsysmt import __quantities_form__
    from numpy import arange, empty, zeros, column_stack
    from molsysmt import box_vectors_from_box_lengths_and_angles
    from molsysmt._private_tools.units import length_unit_name, angle_unit_name, time_unit_name
    from simtk.unit import angstroms, degrees, picoseconds

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all')
    n_atoms = get_n_atoms_from_system(item, indices='all', frame_indices='all')

    step = arange(n_frames, dtype=int)
    time = puw.quantity(zeros(n_frames, dtype=float), 'picoseconds', __quantities_form__)
    xyz = column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    xyz = xyz.reshape([-1, item.num_atoms, 3])
    xyz = puw.quantity(xyz,'angstroms', __quantities_form__)

    if item.unit_cell is not None:

        cell_lengths = empty([n_frames,3], dtype='float64')
        cell_angles = empty([n_frames,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms', __quantities_form__)
        cell_angles = puw.quantity(cell_angles, 'degrees', __quantities_form__)

        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        box = puw.convert(box, length_unit_name)

    else:

        box = None

    xyz = puw.convert(xyz, length_unit_name)
    time = puw.convert(time, time_unit_name)

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

