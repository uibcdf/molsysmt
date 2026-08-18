from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:mol2.

    Parameters
    ----------
    item : file:mol2
        Source item in file:mol2 form.

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
        output = item.endswith('.mol2')

    return output

