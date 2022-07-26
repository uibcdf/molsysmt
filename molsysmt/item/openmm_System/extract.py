from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.System')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True):

    if check:

        digest_item(item, 'openmm.System')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.__copy__()
    else:
        raise NotImplementedMethodError()

    return tmp_item

