from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.CharmmPsfFile')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            raise NotImplementedMethodError()
        else:
            tmp_item = item
    else:

        raise NotImplementedMethodError()

    return tmp_item

