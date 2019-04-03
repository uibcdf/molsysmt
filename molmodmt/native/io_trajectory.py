from .trajectory import Trajectory as _Trajectory
import numpy as _np

def parse_mdtraj_Trajectory(item=None, selection=None, frames=None, syntaxis='mdtraj'):

    tmp_coordinates = _np.asfortranarray(item.xyz) # the same array and same units
    tmp_box = _np.asfortranarray(item.unitcell_vectors)
    tmp_time = _np.asfortranarray(item.time)
    try:
        tmp_timestep = item.timestep
    except:
        tmp_timestep = None

    return tmp_coordinates, tmp_box, tmp_time, tmp_timestep

def from_mdtraj_Trajectory(item=None, selection=None, frames=None, syntaxis='mdtraj'):

    tmp_coordinates, tmp_box, tmp_time, tmp_timestep = parse_mdtraj_Trajectory(item,
                                                                               selection=selection,
                                                                               frames=frames,
                                                                               syntaxis=syntaxis)
    tmp_molmod_trajectory = _Trajectory(filename=item)
    tmp_molmod_trajectory._initialize_with_coors(coordinates=tmp_coordinates, box=tmp_box, time=tmp_time,
                      timestep=tmp_timestep)
    return tmp_molmod_trajectory

def to_mdtraj_Trajectory(item=None, selection=None, frames=None, syntaxis='mdtraj'):
    from mdtraj import Trajectory as _mdtraj_Trajectory
    tmp_mdtraj_trajectory_item = _mdtraj_Trajectory(item.coordinates,item.topology_mdtraj)
    tmp_mdtraj_trajectory_item.unitcell_vectors = _np.ascontiguousarray(item.box)
    tmp_mdtraj_trajectory_item.time = _np.ascontiguousarray(item.time)
    del(_mdtraj_Trajectory)
    return tmp_mdtraj_trajectory_item

def from_xtc(item=None, topology=None, selection=None, frames=None, syntaxis='mdtraj'):
    from molmodmt import extract as _extract
    tmp_item = _Trajectory(filename=item, topology=topology)
    if frames is not None:
        tmp_item.load(frames=frames, selection=selection, syntaxis=syntaxis)
    return tmp_item
