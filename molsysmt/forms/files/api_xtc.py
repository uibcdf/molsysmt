from os.path import basename as _basename
from molsysmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'xtc': form_name
    }

info=["",""]
with_topology=False
with_trajectory=True

def to_mdtraj_Trajectory(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt import convert, select

    if topology is None:
        raise BadCallError(BadCallMessage)

    if frame_indices is None:
        raise BadCallError(BadCallMessage)

    tmp_topology = convert(topology, to_form='mdtraj.Topology')

    if frame_indices == 'all':

        from mdtraj import load as _mdtraj_load
        tmp_form = _mdtraj_load(item, top=tmp_topology, atom_indices=atom_indices)
        del(_mdtraj_load)

    else:

        from mdtraj import load_frame as _mdtraj_load_frame

        if hasattr(frame_indices, '__iter__'):
            tmp_form = _mdtraj_load_frame(item, frame_indices[0], top=tmp_topology, atom_indices=atom_indices)
            for ii in frame_indices[1:]:
                aux_form = _mdtraj_load_frame(item, ii, top=tmp_topology, atom_indices=atom_indices)
                tmp_form = tmp_form.join(aux_form, check_topology=False, discard_overlapping_frames=False)

        else:

            tmp_form = _mdtraj_load_frame(item, frame_indices, top=tmp_topology, atom_indices=atom_indices)

        del(_mdtraj_load_frame)

    return tmp_form

def to_parmed_Structure(item, topology=None, atom_indices='all', frame_indices='all'):

    return to_parmed_GromacsTopologyFile(item, topology, atom_indices='all', frame_indices='all')

def to_parmed_GromacsTopologyFile(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt import extract as _extract
    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    tmp_item=_parmed_from_gromacs(topology)
    tmp_item=_extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_MolSys(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_xtc
    return from_xtc(item, topology=topology, atom_indices=atom_indices, frame_indices=frame_indices)

def to_mdtraj_XTCTrajectoryFile(item, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import XTCTrajectoryFile
    return XTCTrajectoryFile(item)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

#### Get

def get_frames_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='atom', indices=indices,
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

# System

def get_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='system',
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    n_frames = get(tmp_item, target='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    n_atoms = get(tmp_item, target='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

