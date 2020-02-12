from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory import Trajectory as _molmodmt_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Trajectory : form_name,
    'molmodmt.Trajectory' : form_name
}

# Methods

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):
    from molmodmt.native.io_trajectory import to_mdtraj_Trajectory as molmodmt_Trajectory_to_mdtraj_Trajectory
    return molmodmt_Trajectory_to_mtraj_Trajectory(item, selection=atom_indices, frame_indices=frame_indices, syntaxis=syntaxis)

def to_parmed_GromacsTopologyFile(item, atom_indices='all', frame_indices='all'):
    from .api_mdtraj_Topology import to_parmed_GromacsTopologyFile as mdtraj_Topology_to_parmed_GromacsTopologyFile
    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return mdtraj_Topology_to_GromacsTopologyFile(tmp_item)

def to_xtc(item, output_file_path=None, atom_indices='all', frame_indices='all'):
    from .api_mdtraj_Trajectory import to_xtc as mdtraj_Trajectory_to_xtc
    tmp_item=to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return mdtraj_Trajectory_to_xtc(tmp_item, output_file_path=output_file_path)

def to_top(item, output_file_path=None, atom_indices='all', frame_indices='all'):
    from .api_mdtraj_Topology import to_top as mdtraj_Topology_to_top
    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return mdtraj_Topology_to_top(tmp_item, output_file_path=output_file_path)

def select_with_MDTraj(item, selection):
    from .api_mdtraj_Topology import select_with_MDTraj as _select_with_MDTraj
    return _select_with_MDTraj(item.topology_mdtraj,selection)

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Trajectory import to_nglview as mdtraj_to_nglview
    tmp_item = to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return _mdtraj_to_nglview(tmp_item)

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def duplicate(item):

    return item.duplicate()

###### Get

## atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_coordinates = item.coordinates

    if frame_indices is not 'all':
        tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    if indices is not 'all':
        tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates

## group

## chain

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return item.n_frames

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    return item.coordinates[frame_indices]

def get_box_from_system(item, indices='all', frame_indices='all'):

    return item.box[frame_indices]

def get_time_from_system(item, indices='all', frame_indices='all'):

    return item.time[frame_indices]

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

