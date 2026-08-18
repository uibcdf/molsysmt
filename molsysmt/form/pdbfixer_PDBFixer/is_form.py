
def is_form(item):
    """
    Checking whether an item is an instance of form pdbfixer.PDBFixer.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form pdbfixer.PDBFixer, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'pdbfixer.pdbfixer.PDBFixer')

    return output

