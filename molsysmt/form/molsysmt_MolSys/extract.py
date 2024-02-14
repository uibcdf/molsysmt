from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSys')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    return item.extract(atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all,
                        skip_digestion=True)
    
