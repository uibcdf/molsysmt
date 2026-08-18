def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.Structures.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.Structures, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.structures.Structures')

    return output

