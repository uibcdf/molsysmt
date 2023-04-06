from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:psf')
def merge(items, atom_indices='all'):

    raise NotImplementedMethodError()

