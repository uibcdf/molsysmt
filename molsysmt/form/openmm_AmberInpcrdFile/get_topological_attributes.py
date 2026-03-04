from molsysmt._private.arg_digestion import arg_digest
import types

form='openmm.AmberInpcrdFile'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.getNumAtoms()

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
