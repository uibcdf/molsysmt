import types

import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


form = 'file:xyznpy'


def _read_shape(item):
    with open(item, 'rb') as file:
        return tuple(int(value) for value in np.load(file))


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form file:xyznpy.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _read_shape(item)[1]


@arg_digest(form=form)
def get_atom_index_from_atom(
    item, indices='all', structure_indices='all', skip_digestion=False
):
    """
    Getting atom index from atom in form file:xyznpy.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = np.arange(_read_shape(item)[1], dtype=int)
    if not is_all(indices):
        output = output[indices]
    return output.tolist()


__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith('get_')
]
