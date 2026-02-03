from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.dependencies import requires

@arg_digest(form='openmm.System')
@requires('openmm')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.__copy__()
    else:
        raise NotImplementedMethodError()

    return tmp_item

