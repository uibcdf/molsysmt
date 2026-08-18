from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

    return item.copy()

