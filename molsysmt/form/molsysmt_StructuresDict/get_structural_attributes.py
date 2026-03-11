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
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    structure_id = item.get('structure_id', None)
    if structure_id is None:
        return None

    structure_id = copy(structure_id)
    if is_all(structure_indices):
        return structure_id
    return structure_id[structure_indices]


@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):
    velocities = item.get('velocities', None)
    if velocities is None:
        return None

    velocities = copy(velocities)
    if is_all(structure_indices):
        return velocities
    return velocities[structure_indices, :, :]


@arg_digest(form=form)
def get_b_factor_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    b_factor = item.get('b_factor', None)
    if b_factor is None:
        return None

    b_factor = copy(b_factor)
    if not is_all(structure_indices):
        b_factor = b_factor[structure_indices, :]
    if not is_all(indices):
        b_factor = b_factor[:, indices]
    return b_factor


@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):
    return get_b_factor_from_atom(item, structure_indices=structure_indices, skip_digestion=True)

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
