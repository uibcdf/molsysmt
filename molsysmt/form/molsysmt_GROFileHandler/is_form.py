
def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.GROFileHandler.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.GROFileHandler, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.gro_file_handler.GROFileHandler')

    return output

