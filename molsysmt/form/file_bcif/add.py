from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:bcif', to_form='file:bcif')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

