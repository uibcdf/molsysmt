from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.Topology')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True):

    if is_all(atom_indices):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract()

    return tmp_item

