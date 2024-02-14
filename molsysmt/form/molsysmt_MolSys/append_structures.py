from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def append_structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    item.append_structures(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    pass

