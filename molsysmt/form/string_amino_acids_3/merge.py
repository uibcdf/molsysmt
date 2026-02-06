from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:amino_acids_3')
def merge(items, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

