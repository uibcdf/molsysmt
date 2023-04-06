from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer', to_form='pdbfixer.PDBFixer')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

