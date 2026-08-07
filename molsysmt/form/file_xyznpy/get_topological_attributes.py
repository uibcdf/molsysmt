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
    return _read_shape(item)[1]


@arg_digest(form=form)
def get_atom_index_from_atom(
    item, indices='all', structure_indices='all', skip_digestion=False
):
    output = np.arange(_read_shape(item)[1], dtype=int)
    if not is_all(indices):
        output = output[indices]
    return output.tolist()


__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith('get_')
]
