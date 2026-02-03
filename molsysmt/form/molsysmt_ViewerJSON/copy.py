from molsysmt._private.digestion import arg_digest
from copy import deepcopy


@arg_digest(form='molsysmt.ViewerJSON')
def copy(item, skip_digestion=False):
    """Deep copy a ViewerJSON object."""
    return deepcopy(item)
