from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:cif.gz', to_form='file:cif.gz')
def add(to_item, item, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

