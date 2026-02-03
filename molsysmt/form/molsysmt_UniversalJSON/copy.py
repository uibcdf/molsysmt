from molsysmt._private.arg_digestion import arg_digest
from copy import deepcopy


@arg_digest(form='molsysmt.UniversalJSON')
def copy(item, skip_digestion=False):
    """Deep copy a UniversalJSON object."""
    return deepcopy(item)
