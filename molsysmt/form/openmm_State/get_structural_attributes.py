import types

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = 'openmm.State'


def _as_rank_three(quantity):
    unit = puw.get_unit(quantity)
    values = np.asarray(puw.get_value(quantity))
    return puw.standardize(values[np.newaxis, :, :] * unit)


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    if indices is None or structure_indices is None:
        return None

    output = _as_rank_three(item.getPositions(asNumpy=True))
    if not is_all(structure_indices):
        output = output[structure_indices, :, :]
    if not is_all(indices):
        output = output[:, indices, :]
    return output


@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    if indices is None or structure_indices is None:
        return None

    output = _as_rank_three(item.getVelocities(asNumpy=True))
    if not is_all(structure_indices):
        output = output[structure_indices, :, :]
    if not is_all(indices):
        output = output[:, indices, :]
    return output


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    return get_coordinates_from_atom(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):
    return get_velocities_from_atom(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    if structure_indices is None:
        return None

    output = _as_rank_three(item.getPeriodicBoxVectors(asNumpy=True))
    if not is_all(structure_indices):
        output = output[structure_indices, :, :]
    return output


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    if structure_indices is None:
        return None

    time = item.getTime()
    output = puw.standardize(np.asarray([puw.get_value(time)]) * puw.get_unit(time))
    if not is_all(structure_indices):
        output = output[structure_indices]
    return output


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    return None


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    if structure_indices is None:
        return 0
    if is_all(structure_indices):
        return 1
    return len(structure_indices)


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
