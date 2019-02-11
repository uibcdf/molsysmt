from .trajectory import Trajectory as _Trajectory
from numpy import asfortranarray as _asfortranarray

def from_mdtraj_Trajectory(item=None):

    tmp_coordinates = _asfortranarray(item.xyz) # the same array and same units
    tmp_box = _asfortranarray(item.unitcell_vectors)
    tmp_time = _asfortranarray(item.time)
    try:
        tmp_timestep = _asfortranarray(item.timestep)
    except:
        tmp_timestep = None

    return _Trajectory(coordinates=tmp_coordinates, box=tmp_box, time=tmp_time,
                      timestep=tmp_timestep)
