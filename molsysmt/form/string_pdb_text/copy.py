from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:pdb_text.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.


    .. versionadded:: 1.0.0
    """

    from copy import copy
    tmp_item = copy(item)

    return tmp_item

