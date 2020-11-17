import numpy as np
from os.path import basename as basename
from simtk.openmm.app import GromacsGroFile as _openmm_GromacsGroFile
import simtk.unit as unit

form_name=basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_GromacsGroFile : form_name,
    'openmm.GromacsGroFile' : form_name
}

info=["",""]
with_topology=True
with_trajectory=True

def load_frame (item, atom_indices='all', frame_indices='all'):

    # It doesn't really work. seek doesn't work. Once the file is read can not be rewinded.

    step = None
    time = None

    if frame_indices is 'all':

        n_frames = get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    coordinates_list = []
    box_list = []

    for ii in frame_indices:

        coordinates_list.append(item.getPositions(asNumpy=True, frame=ii)._value)
        box=item.getPeriodicBoxVectors(frame=ii)
        box=np.array(box._value)
        box_list.append(box)


    coordinates = np.concatenate(coordinates_list)
    box = np.concatenate(box_list)
    del(coordinates_list, box_list)

    if len(box)==0:
        box = None
    else:
        if len(box.shape)==2:
            box = box.reshape(1, box.shape[0], box.shape[1])
        box = box*unit.nanometer

    if len(coordinates.shape)==2:
        coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])
    coordinates = coordinates*unit.nanometer

    return step, time, coordinates, box

def to_molsysmt_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)
    return tmp_item

def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    return item.topology

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import _select

    tmp_item = to_molsysmt_Topology(item)
    atom_indices = _select(tmp_item, selection)
    return atom_indices

##### Set

## Atom

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    step, time, coordinates, box = load_frame(item, atom_indices=indices, frame_indices=frame_indices)
    return step, time, coordinates, box

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    step, time, coordinates, box = load_frame(item, frame_indices=frame_indices)
    return step, time, coordinates, box

def get_n_atoms_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system(item)
    else:
        return len(indices)

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    return get_n_frames_from_system(item, frame_indices=frame_indices)

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return get_form_from_system(item)

## System

def get_frame_from_system(item, indices='all', frame_indices='all'):

    step, time, coordinates, box = load_frame(item, frame_indices=frame_indices)
    return step, time, coordinates, box

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return len(item.atomNames)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        return item.getNumFrames()
    else:
        return len(frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

