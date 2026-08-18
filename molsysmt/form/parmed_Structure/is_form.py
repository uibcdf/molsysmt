def is_form(item):
    """
    Checking whether an item is an instance of form parmed.Structure.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form parmed.Structure, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'parmed.structure.Structure')

    return output

