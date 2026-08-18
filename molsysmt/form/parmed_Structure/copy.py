from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form parmed.Structure.

    Parameters
    ----------
    item : parmed.Structure
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.Structure
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

