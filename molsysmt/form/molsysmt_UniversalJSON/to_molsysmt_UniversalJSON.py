from molsysmt._private.digestion import arg_digest
from copy import deepcopy


@arg_digest(form='molsysmt.UniversalJSON')
def to_molsysmt_UniversalJSON(item, skip_digestion=False):
    """Return a deep-copied UniversalJSON (identity conversion)."""
    return deepcopy(item)
