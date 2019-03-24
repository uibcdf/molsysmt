from .trajectory import Trajectory as _Trajectory
import numpy as _np

def parse_mdtraj_Trajectory(item=None):

    tmp_coordinates = _np.asfortranarray(item.xyz) # the same array and same units
    tmp_box = _np.asfortranarray(item.unitcell_vectors)
    tmp_time = _np.asfortranarray(item.time)
    try:
        tmp_timestep = _np.asfortranarray(item.timestep)
    except:
        tmp_timestep = None

    return tmp_coordinates, tmp_box, tmp_time, tmp_timestep

def from_mdtraj_Trajectory(item=None):

    tmp_coordinates, tmp_box, tmp_time, tmp_timestep = parse_mdtraj_Trajectory(item)

    tmp_molmod_trajectory = _Trajectory(filename=item)
    tmp_molmod_trajectory._initialize_with_coors(coordinates=tmp_coordinates, box=tmp_box, time=tmp_time,
                      timestep=tmp_timestep)
    return tmp_molmod_trajectory

def to_mdtraj_Trajectory(item=None):
    from mdtraj import Trajectory as _mdtraj_Trajectory
    tmp_mdtraj_trajectory_item = _mdtraj_Trajectory(item.coordinates,item.topology_mdtraj)
    tmp_mdtraj_trajectory_item.unitcell_vectors = _np.ascontiguousarray(item.box)
    tmp_mdtraj_trajectory_item.time = _np.ascontiguousarray(item.time)
    if item.timestep is not None:
        tmp_mdtraj_trajectory_item.timestep = _np.ascontiguousarray(item.timestep)
    del(_mdtraj_Trajectory)
    return tmp_mdtraj_trajectory_item

def from_xtc(item=None):

    tmp_molmod_trajectory = _Trajectory(filename=item)
    return tmp_molmod_trajectory
