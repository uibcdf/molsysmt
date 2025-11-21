from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.UniversalJSON')
def copy(item, skip_digestion=False):
    """Deep copy a UniversalJSON object."""
    return deepcopy(item)
