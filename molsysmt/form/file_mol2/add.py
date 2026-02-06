from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:mol2', to_form='file:mol2')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

