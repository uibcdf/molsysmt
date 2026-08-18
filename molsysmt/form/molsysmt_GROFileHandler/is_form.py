
def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.GROFileHandler.

    Parameters
    ----------
    item : molsysmt.GROFileHandler
        Source item in molsysmt.GROFileHandler form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.gro_file_handler.GROFileHandler')

    return output

