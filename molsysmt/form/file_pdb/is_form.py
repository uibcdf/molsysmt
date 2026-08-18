from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:pdb.

    Parameters
    ----------
    item : file:pdb
        Source item in file:pdb form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        output = item.endswith('.pdb')

    return output

