from os.path import basename as _basename
from molmodmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'xtc': form_name
    }

def to_mdtraj_Trajectory(item, topology=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
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

def to_parmed(item, topology=None, selection='all', syntaxis='MDTraj'):
    return to_parmed_GromacsTopologyFile(item, topology, selection=selection, syntaxis=syntaxis)

def to_parmed_Structure(item, topology=None, selection='all', syntaxis='MDTraj'):
    return to_parmed_GromacsTopologyFile(item, topology, selection=selection, syntaxis=syntaxis)

def to_parmed_GromacsTopologyFile(item, topology=None, selection='all', syntaxis='MDTraj'):
    from molmodmt import extract as _extract
    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    tmp_item=_parmed_from_gromacs(topology)
    tmp_item=_extract(tmp_item,selection=selection,syntaxis=syntaxis)
    return tmp_item

def to_molmodmt_MolMod(item, topology=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
    from molmodmt.native.io_molmod import from_xtc
    return from_xtc(item, topology=topology, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

def to_mdtraj_XTCTrajectoryFile(item, selection='all', syntaxis='MDTraj'):

    from mdtraj.formats import XTCTrajectoryFile
    return XTCTrajectoryFile(item)

