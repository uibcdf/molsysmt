from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.ViewerJSON')
def copy(item, skip_digestion=False):
    """Deep copy a ViewerJSON object."""
    return deepcopy(item)
