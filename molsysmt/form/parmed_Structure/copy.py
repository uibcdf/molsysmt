from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form parmed.Structure.

    Parameters
    ----------
    item : parmed.Structure
        Source item in parmed.Structure form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Resulting object in parmed.Structure form.

    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

