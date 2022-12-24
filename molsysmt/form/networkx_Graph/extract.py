from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='networkx.Graph')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, digest=True):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
         tmp_item = item.copy()
        else:
            tmp_item = item.subgraph(atom_indices).copy()
    else:

        tmp_item = item
        if not is_all(atom_indices):
            tmp_item = tmp_item.atom_slice(atom_indices)
        if not is_all(structure_indices):
            tmp_item = tmp_item.slice(structure_indices)

    return tmp_item

