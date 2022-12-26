from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='XYZ')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, digest=True):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from . import get_coordinates_from_atom

        tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, digest=False)

    return tmp_item

