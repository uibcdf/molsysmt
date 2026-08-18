from molsysmt.native import TopologyDict


def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.TopologyDict.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    .. versionadded:: 1.0.0
    """
    return isinstance(item, TopologyDict)
