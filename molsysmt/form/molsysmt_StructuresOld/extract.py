from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.StructuresOld')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

