from molsysmt._private.argdigest import arg_digest
from copy import copy

@arg_digest(form='string:amino_acids_3')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:amino_acids_3.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.


    .. versionadded:: 1.0.0
    """

    return copy(item)

