from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Copied item.
    """

    return item.copy()

