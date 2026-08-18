from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:pdb_text.

    Parameters
    ----------
    item : string:pdb_text
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:pdb_text
        Copied item.
    """

    from copy import copy
    tmp_item = copy(item)

    return tmp_item

