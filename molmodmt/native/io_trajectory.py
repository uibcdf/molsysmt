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


def from_pdb(item=None, selection=None, frames=None, syntaxis='mdtraj'):

    from molmodmt import convert as _convert
    tmp_item = _convert(item, form='mdtraj.Trajectory', selection=selection, syntaxis=syntaxis)
    tmp_item = from_mdtraj_Trajectory(tmp_item)
    return tmp_item

def from_xtc(item=None, topology=None, selection=None, frames=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    tmp_item = _Trajectory(filename=item, topology=topology)
    if frames is not None:
        tmp_item.load(frames=frames, selection=selection, syntaxis=syntaxis)
    return tmp_item

