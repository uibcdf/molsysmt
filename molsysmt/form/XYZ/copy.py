from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='XYZ')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form XYZ.

    Parameters
    ----------
    item : XYZ
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    XYZ
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

