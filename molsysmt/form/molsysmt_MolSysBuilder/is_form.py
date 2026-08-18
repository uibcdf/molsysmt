from molsysmt.native import MolSysBuilder


def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.MolSysBuilder, False otherwise.
    """
    return isinstance(item, MolSysBuilder)
