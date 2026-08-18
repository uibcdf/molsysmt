from molsysmt.native import MolSysBuilder


def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.MolSysBuilder.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Source item in molsysmt.MolSysBuilder form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """
    return isinstance(item, MolSysBuilder)
