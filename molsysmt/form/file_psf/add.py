from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest

@arg_digest(form='file:psf', to_form='file:psf')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

