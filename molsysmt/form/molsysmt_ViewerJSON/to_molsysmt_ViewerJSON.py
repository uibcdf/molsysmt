from molsysmt._private.argdigest import arg_digest
from copy import deepcopy


@arg_digest(form='molsysmt.ViewerJSON')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """
    Converting from molsysmt.ViewerJSON to molsysmt.ViewerJSON.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.ViewerJSON
        Resulting object in molsysmt.ViewerJSON form.


    .. versionadded:: 1.0.0
    """
    return deepcopy(item)
