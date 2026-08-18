from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.StructuresDict')
def copy(item):
    """
    Creating a copy of an item of form molsysmt.StructuresDict.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    molsysmt.StructuresDict
        Resulting object in molsysmt.StructuresDict form.


    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item

