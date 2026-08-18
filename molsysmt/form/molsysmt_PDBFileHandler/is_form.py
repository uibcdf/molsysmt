
def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : molsysmt.PDBFileHandler
        Source item in molsysmt.PDBFileHandler form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.pdb_file_handler.PDBFileHandler')

    return output

