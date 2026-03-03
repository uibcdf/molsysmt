#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np
from molsysmt._private.variables import is_all

import types

form='openmm.Simulation'

## From atom

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    state = item.context.getState(getPositions=True)
    coordinates = state.getPositions(asNumpy=True)
    coordinates = puw.standardize(coordinates)
    coordinates = puw.reshape(coordinates, shape=(1, -1, 3))

    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices,:,:]

    if not is_all(indices):
        coordinates = coordinates[:,indices,:]

    return coordinates

## From system

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    return 1

@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    coordinates = item.context.getState(getPositions=True).getPositions(asNumpy=True)
    unit = puw.get_unit(coordinates)
    coordinates = puw.get_value(coordinates)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices,:,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    state = item.context.getState()
    box = state.getPeriodicBoxVectors(asNumpy=True)

    if box is not None:
        box = puw.standardize(box)
        box = puw.reshape(box, shape=(1, 3, 3))
        if not is_all(structure_indices):
            box = box[structure_indices,:,:]

    return box

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    output = item.context.getState().getTime()
    value = puw.get_value(output)
    unit = puw.get_unit(output)
    output = np.array([value])*unit
    output = puw.standardize(output)

    return output

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

