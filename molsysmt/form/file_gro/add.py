from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:gro', to_form='file:gro')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

