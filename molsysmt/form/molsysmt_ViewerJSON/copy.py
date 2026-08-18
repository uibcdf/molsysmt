from molsysmt._private.argdigest import arg_digest
from copy import deepcopy


@arg_digest(form='molsysmt.ViewerJSON')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.ViewerJSON.

    Parameters
    ----------
    item : molsysmt.ViewerJSON
        Source item in molsysmt.ViewerJSON form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.ViewerJSON
        Resulting object in molsysmt.ViewerJSON form.

    .. versionadded:: 1.0.0
    """
    return deepcopy(item)
