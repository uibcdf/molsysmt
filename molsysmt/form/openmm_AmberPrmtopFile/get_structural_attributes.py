from molsysmt._private.arg_digestion import arg_digest
import types

form='openmm.AmberPrmtopFile'

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    return 0

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    return None

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
