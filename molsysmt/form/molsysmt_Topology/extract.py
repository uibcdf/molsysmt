from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.Topology')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices):
        if copy_if_all:
            tmp_item = item.copy()
        else:
            tmp_item = item
    else:
        tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

