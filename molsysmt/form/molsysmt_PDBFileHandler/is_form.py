
def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form molsysmt.PDBFileHandler, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.pdb_file_handler.PDBFileHandler')

    return output

