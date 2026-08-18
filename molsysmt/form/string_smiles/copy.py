from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:smiles')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:smiles
        Resulting object in string:smiles form.

    .. versionadded:: 1.0.0
    """

    from copy import copy as _copy
    return _copy(item)
