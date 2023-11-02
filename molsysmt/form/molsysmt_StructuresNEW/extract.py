from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.StructuresNEW')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True):

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

