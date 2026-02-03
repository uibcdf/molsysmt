from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='biopython.Seq')
def merge(items, group_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

