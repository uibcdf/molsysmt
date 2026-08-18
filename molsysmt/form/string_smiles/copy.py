from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:smiles')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:smiles
        Copied item.
    """

    from copy import copy as _copy
    return _copy(item)
