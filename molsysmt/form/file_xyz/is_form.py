from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:xyz.

    Parameters
    ----------
    item : file:xyz
        Source item in file:xyz form.

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
        output = item.endswith('.xyz')

    return output
