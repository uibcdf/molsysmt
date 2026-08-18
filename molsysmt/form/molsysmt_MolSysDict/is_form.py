from molsysmt.native import MolSysDict


def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.MolSysDict.

    Parameters
    ----------
    item : molsysmt.MolSysDict
        Source item in molsysmt.MolSysDict form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """
    return isinstance(item, MolSysDict)
