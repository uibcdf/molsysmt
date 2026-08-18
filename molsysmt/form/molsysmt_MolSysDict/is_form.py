from molsysmt.native import MolSysDict


def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.MolSysDict.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.MolSysDict, False otherwise.
    """
    return isinstance(item, MolSysDict)
