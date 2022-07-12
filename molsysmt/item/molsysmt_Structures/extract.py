from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.variables import is_all

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'molsysmt.Structures')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

