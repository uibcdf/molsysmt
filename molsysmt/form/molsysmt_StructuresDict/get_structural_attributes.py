from copy import copy

from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.StructuresDict'


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    coordinates = copy(item['coordinates'])

    if not is_all(structure_indices):
        if not is_all(indices):
            coordinates = coordinates[np.ix_(structure_indices, indices)]
        else:
            coordinates = coordinates[structure_indices, :, :]
    elif not is_all(indices):
        coordinates = coordinates[:, indices, :]

    return coordinates


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    if is_all(structure_indices):
        return item['coordinates'].shape[0]
    return len(structure_indices)


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    coordinates = copy(item['coordinates'])
    if is_all(structure_indices):
        return coordinates
    return coordinates[structure_indices, :, :]


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    box = item.get('box', None)
    if box is None:
        return None

    box = copy(box)
    if is_all(structure_indices):
        return box
    return box[structure_indices, :, :]


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    time = item.get('time', None)
    if time is None:
        return None

    time = copy(time)
    if is_all(structure_indices):
        return time
    return time[structure_indices]


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
