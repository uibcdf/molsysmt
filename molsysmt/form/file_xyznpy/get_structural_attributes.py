from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form = 'file:xyznpy'


def _read_shape(item):
    with open(item, 'rb') as file:
        return tuple(int(value) for value in np.load(file))


def _read_coordinates(item):
    with open(item, 'rb') as file:
        np.load(file)
        coordinates = np.load(file)
    return puw.standardize(coordinates * puw.unit('nm'))


@arg_digest(form=form)
def get_n_structures_from_system(
    item, structure_indices='all', skip_digestion=False
):
    if is_all(structure_indices):
        return _read_shape(item)[0]
    return len(structure_indices)


@arg_digest(form=form)
def get_structure_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    output = np.arange(_read_shape(item)[0], dtype=int)
    if not is_all(structure_indices):
        output = output[structure_indices]
    return output.tolist()


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    if indices is None or structure_indices is None:
        return None

    output = _read_coordinates(item)
    if not is_all(structure_indices):
        if not is_all(indices):
            output = output[np.ix_(structure_indices, indices)]
        else:
            output = output[structure_indices, :, :]
    elif not is_all(indices):
        output = output[:, indices, :]
    return output


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    if structure_indices is None:
        return None

    output = _read_coordinates(item)
    if not is_all(structure_indices):
        output = output[structure_indices, :, :]
    return output


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
