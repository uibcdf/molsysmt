from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm import Context as _openmm_Context
from molsysmt.molecular_system import molecular_system_components

form_name='openmm.Context'

is_form={
    _openmm_Context : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['topology', 'coordinates', 'box', 'bonds', 'ff_parameters', 'mm_paremeters']:
    has[ii]=True

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def get_n_atoms_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        return item.getSystem().getNumParticles()
    else:
        len(indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from numpy import array as _array

    coordinates = item.getState(getPositions=True).getPositions(asNumpy=True)
    units = coordinates.unit
    coordinates=coordinates._value
    coordinates = coordinates.reshape([1, coordinates.shape[0], coordinates.shape[1]])

    if frame_indices is not 'all':
        coordinates = coordinates[frame_indices,:,:]

    if indices is not 'all':
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * units

    return coordinates

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.getSystem().getNumParticles()

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array

    coordinates = item.getState(getPositions=True).getPositions(asNumpy=True)
    units = coordinates.unit
    coordinates = coordinates._value
    coordinates = coordinates.reshape([1, coordinates.shape[0], coordinates.shape[1]])

    if frame_indices is not 'all':
        coordinates = coordinates[frame_indices,:,:]

    coordinates = coordinates * units

    return coordinates

def get_box_from_system(item, indices='all', frame_indices='all'):

    box = item.getState().getPeriodicBoxVectors(asNumpy=True)
    units = box.unit
    box = box._value
    box = box.reshape([1, box.shape[0], box.shape[1]])

    if frame_indices is not 'all':
        box = box[frame_indices,:,:]

    box = box * units

    return box

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_shape_from_box_vectors
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    return box_shape_from_box_vectors(box)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_lengths_from_box_vectors
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    return box_lengths_from_box_vectors(box)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_angles_from_box_vectors
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    return box_angles_from_box_vectors(box)

def get_time_from_system(item, indices='all', frame_indices='all'):

    time = item.getState().getTime()
    return time

def get_step_from_system(item, indices='all', frame_indices='all'):

    return None

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    return item.setPositions(value[0])

