from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_text', to_form='string:pdb_text')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

