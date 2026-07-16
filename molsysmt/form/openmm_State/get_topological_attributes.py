import types

from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

form = 'openmm.State'


def _get_n_atoms(item):
    return len(item.getPositions())


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    if is_all(indices):
        return list(range(_get_n_atoms(item)))
    return list(indices)


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return _get_n_atoms(item)


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
