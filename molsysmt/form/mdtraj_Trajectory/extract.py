from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='mdtraj.Trajectory')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        tmp_item = item
        if not is_all(atom_indices):
            tmp_item = tmp_item.atom_slice(atom_indices)
        if not is_all(structure_indices):
            tmp_item = tmp_item.slice(structure_indices)

    return tmp_item

