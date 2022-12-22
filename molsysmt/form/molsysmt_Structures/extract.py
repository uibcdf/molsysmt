from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.Structures')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, digest=True):

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, structure_indices=structure_indices, digest=False)

    return tmp_item

