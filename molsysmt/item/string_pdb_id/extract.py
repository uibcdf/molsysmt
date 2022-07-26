from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='string:pdb_id')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if is_all(atom_indices) and is_all(structure_indices):

        raise NotImplementedMethodError()

    else:

        raise NotImplementedMethodError()

    return tmp_item

