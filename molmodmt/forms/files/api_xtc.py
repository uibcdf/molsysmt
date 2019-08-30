from os.path import basename as _basename
from molmodmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'xtc': form_name
    }

def to_mdtraj_Trajectory(item, topology=None, selection=None, frame_indices='all', syntaxis='MDTraj'):
    from molmodmt import extract as _extract
    from mdtraj import load as _mdtraj_load

    if topology is None:
        raise BadCallError(BadCallMessage)

    tmp_form = _mdtraj_load(item, top=topology)
    tmp_form = _extract(tmp_form,selection=selection,syntaxis=syntaxis)
    del(_mdtraj_load)
    return tmp_form

#def to_molmod(item, topology=None, selection=None, frames=None, syntaxis='mdtraj'):
#    return to_molmodmt_MolMod(item,topology,selection=selection,syntaxis=syntaxis,frames=frames)

def to_parmed(item, topology=None, selection=None, syntaxis='MDTraj'):
    return to_parmed_GromacsTopologyFile(item, topology, selection=selection, syntaxis=syntaxis)

def to_parmed_Structure(item, topology=None, selection=None, syntaxis='MDTraj'):
    return to_parmed_GromacsTopologyFile(item, topology, selection=selection, syntaxis=syntaxis)

def to_parmed_GromacsTopologyFile(item, topology=None, selection=None, syntaxis='MDTraj'):
    from molmodmt import extract as _extract
    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    tmp_item=_parmed_from_gromacs(topology)
    tmp_item=_extract(tmp_item,selection=selection,syntaxis=syntaxis)
    return tmp_item

def to_molmodmt_MolMod(item, topology=None, selection=None, frame_indices=None, syntaxis='MDTraj'):
    from molmodmt.native.io_molmod import from_xtc
    return from_xtc(item, topology=topology, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

def to_mdtraj_XTCTrajectoryFile(item, selection=None, syntaxis='MDTraj'):

    from mdtraj.formats import XTCTrajectoryFile
    return XTCTrajectoryFile(item)

#### Get

def get_frames_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, element='atom', indices=indices,
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

# System

def get_frames_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, element='system',
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_frames_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    n_frames = get(tmp_item, element='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    n_atoms = get(tmp_item, element='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms



