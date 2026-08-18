
def is_form(item):
    """
    Checking whether an item is an instance of form openmm.Modeller.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form openmm.Modeller, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'openmm.app.modeller.Modeller')

    return output

