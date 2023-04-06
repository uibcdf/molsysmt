from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:inpcrd', to_form='file:inpcrd')
def add(to_item, item, atom_indices='all', structure_indices='all'):

    raise NotImplementedMethodError()

