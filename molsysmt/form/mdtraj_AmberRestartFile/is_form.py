
def is_form(item):
    """
    Checking whether an item is an instance of form mdtraj.AmberRestartFile.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form mdtraj.AmberRestartFile, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return item_fullname == 'mdtraj.formats.amberrst.AmberRestartFile'
