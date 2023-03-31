from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def merge(items, atom_indices='all'):

    raise NotImplementedMethodError()

