#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form='openmm.Context'


## From atom

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    coordinates = item.getState(getPositions=True).getPositions(asNumpy=True)
    unit = puw.get_unit(coordinates)
    coordinates = puw.get_value(coordinates)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices,:,:]

    if not is_all(indices):
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates

@digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    velocities = item.getState(getVelocities=True).getVelocities(asNumpy=True)
    unit = puw.get_unit(velocities)
    velocities = puw.get_value(velocities)
    velocities = velocities.reshape(1, velocities.shape[0], velocities.shape[1])

    if not is_all(structure_indices):
        velocities = velocities[structure_indices,:,:]

    if not is_all(indices):
        velocities = velocities[:,indices,:]

    velocities = velocities * unit
    velocities = puw.standardize(velocities)

    return velocities

## From group

## From component

## From molecule

## From chain

## From entity

## From system

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    coordinates = item.getState(getPositions=True).getPositions(asNumpy=True)
    unit = puw.get_unit(coordinates)
    coordinates = puw.get_value(coordinates)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices,:,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates

@digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    velocities = item.getState(getVelocities=True).getVelocities(asNumpy=True)
    unit = puw.get_unit(velocities)
    velocities = puw.get_value(velocities)
    velocities = velocities.reshape(1, velocities.shape[0], velocities.shape[1])

    if not is_all(structure_indices):
        velocities = velocities[structure_indices,:,:]

    velocities = velocities * unit
    velocities = puw.standardize(velocities)

    return velocities

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    box=item.getState().getPeriodicBoxVectors(asNumpy=True)

    if box is not None:
        box_unit = box.unit
        box = np.array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box_unit

    output=None

    if box is not None:
        if is_all(structure_indices):
            output=box
        else:
            output=box[structure_indices,:,:]

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    output = item.getState().getTime()
    value = puw.get_value(output)
    unit = puw.get_unit(output)
    output = np.array([value])*unit
    output = puw.standardize(output)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return 1
    else:
        len(structure_indices)

## From bond

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

