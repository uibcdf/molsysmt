from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='parmed.Structure')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from molsysmt._private.atom_indices import atom_indices_to_AmberMask
        from molsysmt._private.atom_indices import complementary_atom_indices
        tmp_atom_indices = complementary_atom_indices(item, atom_indices)
        mask = atom_indices_to_AmberMask(item, tmp_atom_indices)
        tmp_item = copy(item)
        tmp_item.strip(atom_indices2AmberMask(atom_indices,len(item.atoms),inverse=True))

    return tmp_item

