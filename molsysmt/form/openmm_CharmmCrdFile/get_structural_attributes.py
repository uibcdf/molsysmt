#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.CharmmCrdFile'


def _coordinates(item):
    values = np.asarray(puw.get_value(item.positions))
    unit = puw.get_unit(item.positions)
    return puw.standardize(values[np.newaxis, :, :] * unit)


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    if indices is None or structure_indices is None:
        return None
    output = _coordinates(item)
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

# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
