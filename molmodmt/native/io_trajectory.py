from .trajectory import Trajectory as _Trajectory
import numpy as _np

def from_mdtraj_Trajectory(item=None):

    tmp_coordinates = _np.asfortranarray(item.xyz) # the same array and same units
    tmp_box = _np.asfortranarray(item.unitcell_vectors)
    tmp_time = _np.asfortranarray(item.time)
    try:
        tmp_timestep = _np.asfortranarray(item.timestep)
    except:
        tmp_timestep = None

    return _Trajectory(coordinates=tmp_coordinates, box=tmp_box, time=tmp_time,
                      timestep=tmp_timestep)

def to_mdtraj_Trajectory(item=None):
    from mdtraj import Trajectory as _mdtraj_Trajectory
    tmp_mdtraj_trajectory_item = Trajectory(item.trajectory.coordinates,item.topology)
    tmp_mdtraj_trajectory_item.unitcell_vectors = _np.ascontigouousarray(item.trajectory.box)
    tmp_mdtraj_trajectory_item.time = _np.ascontigouousarray(item.trajectory.time)
    tmp_mdtraj_trajectory_item.timestep = _np.ascontigouousarray(item.trajectory.timestep)
    del(_mdtraj_Trajectory)
    return tmp_mdtraj_trajectory_item
