from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices
from molsysmt._private.variables import is_all

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'mdtraj.Trajectory')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

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

