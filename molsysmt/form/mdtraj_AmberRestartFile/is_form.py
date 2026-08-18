
def is_form(item):
    """
    Checking whether an item is an instance of form mdtraj.AmberRestartFile.

    Parameters
    ----------
    item : mdtraj.AmberRestartFile
        Source item in mdtraj.AmberRestartFile form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return item_fullname == 'mdtraj.formats.amberrst.AmberRestartFile'
