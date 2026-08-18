from molsysmt._private.argdigest import arg_digest
from copy import copy

@arg_digest(form='string:amino_acids_3')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:amino_acids_3.

    Parameters
    ----------
    item : string:amino_acids_3
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:amino_acids_3
        Copied item.
    """

    return copy(item)

