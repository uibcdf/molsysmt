from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Structures')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Copied item.
    """

    return item.copy()

