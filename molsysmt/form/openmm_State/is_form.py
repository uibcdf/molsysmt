def is_form(item):
    """
    Checking whether an item is an instance of form openmm.State.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form openmm.State, False otherwise.
    """


    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'openmm.openmm.State')

    return output

