from molsysmt._private.argdigest import arg_digest
from copy import copy

@arg_digest(form='string:amino_acids_1')
def extract(item, skip_digestion=False):

    """
    Extracting a subset of elements or structures from form string:amino_acids_1.

    Parameters
    ----------
    item : string:amino_acids_1
        Source item in string:amino_acids_1 form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.

    .. versionadded:: 1.0.0
    """
    return copy(item)

