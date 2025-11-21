from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.ViewerJSON')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """Return a deep-copied ViewerJSON (identity conversion)."""
    return deepcopy(item)
