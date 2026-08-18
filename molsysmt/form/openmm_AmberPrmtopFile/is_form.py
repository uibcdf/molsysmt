
def is_form(item):
    """
    Checking whether an item is an instance of form openmm.AmberPrmtopFile.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form openmm.AmberPrmtopFile, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return item_fullname=='openmm.app.amberprmtopfile.AmberPrmtopFile'

