from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='parmed.Structure')
def merge(items, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

