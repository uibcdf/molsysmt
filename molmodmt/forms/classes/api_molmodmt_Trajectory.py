from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory import Trajectory as _molmodmt_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Trajectory : form_name,
    'molmodmt.Trajectory' : form_name
}

# Methods

def select_with_MDTraj(item, selection):
    from .api_mdtraj_Topology import select_with_MDTraj as _select_with_MDTraj
    return _select_with_MDTraj(item.topology_mdtraj,selection)

def extract_atom_indices(item, atom_indices):
    return item.extract(atom_indices)

def to_mdtraj_Trajectory(item, selection=None, frame_indices=None, syntaxis="MDTraj"):
    from molmodmt.native.io_trajectory import to_mdtraj_Trajectory as _to_mdtraj_Trajectory
    return _to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj(item, selection=None, frame_indices=None, syntaxis="MDTraj"):
    return to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_parmed_GromacsTopologyFile(item, selection=None, frame_indices=None, syntaxis="MDTraj"):
    from .api_mdtraj_Topology import to_parmed_GromacsTopologyFile as _to_GromacsTopologyFile
    return _to_GromacsTopologyFile(item.topology_mdtraj, selection=selection, syntaxis=syntaxis)

def to_xtc(item,filename=None, selection=None, frame_indices=None, syntaxis="MDTraj"):
    from .api_mdtraj_Trajectory import to_xtc as _to_xtc
    tmp_item=to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)
    return _to_xtc(tmp_item,filename)

def to_top(item,filename=None, selection=None, frame_indices=None, syntaxis="MDTraj"):
    from .api_mdtraj_Topology import to_top as _to_top
    return _to_top(item.topology_mdtraj,filename, selection=selection, syntaxis=syntaxis)

def to_nglview(item, selection=None, frame_indices=None, syntaxis="MDTraj"):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview

    if type(item) in [list,tuple]:
        tmp_item = []
        for ii in item:
            tmp_item.append(to_mdtraj_Trajectory(ii))
    else:
        tmp_item = to_mdtraj_Trajectory(item)

    return _mdtraj_to_nglview(tmp_item)

def duplicate(item):

    from copy import deepcopy
    from molmodmt.native.trajectory import Trajectory
    from .api_molmodmt_TrajectoryFile import duplicate as _duplicate_TrajectoryFile

    tmp_item = Trajectory()

    tmp_item.length_units = deepcopy(item.length_units)
    tmp_item.time_units = deepcopy(item.time_units)

    tmp_item.step = deepcopy(item.step)
    tmp_item.time = deepcopy(item.time)
    tmp_item.coordinates = deepcopy(item.coordinates)
    tmp_item.box = deepcopy(item.box)
    tmp_item.box_shape = deepcopy(item.box_shape)

    tmp_item.n_frames = deepcopy(item.n_frames)
    tmp_item.n_atoms = deepcopy(item.n_atoms)

    tmp_item.file = _duplicate_TrajectoryFile(item.file)

    return tmp_item

###### Get

## atom

def get_coordinates_from_atom(item, indices=None, frame_indices=None):

    tmp_coordinates = item.coordinates[frame_indices]
    tmp_coordinates = tmp_coordinates[:, indices, :]
    return tmp_coordinates

## residue

## chain

## system

def get_n_atoms_from_system(item, indices=None, frame_indices=None):

    return item.n_atoms

def get_n_frames_from_system(item, indices=None, frame_indices=None):

    return item.n_frames

def get_coordinates_from_system(item, indices=None, frame_indices=None):

    return item.coordinates[frame_indices]

def get_box_from_system(item, indices=None, frame_indices=None):

    return item.box[frame_indices]

def get_time_from_system(item, indices=None, frame_indices=None):

    return item.time[frame_indices]

