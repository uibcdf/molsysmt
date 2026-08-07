from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import types

form='openmm.AmberInpcrdFile'

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    if is_all(indices):
        return list(range(item.getNumAtoms()))
    return list(indices)


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.getNumAtoms()

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
