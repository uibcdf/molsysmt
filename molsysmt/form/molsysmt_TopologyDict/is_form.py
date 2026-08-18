from molsysmt.native import TopologyDict


def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.TopologyDict.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.TopologyDict, False otherwise.
    """
    return isinstance(item, TopologyDict)
