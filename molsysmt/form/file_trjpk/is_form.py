from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:trjpk.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form file:trjpk, False otherwise.
    """

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        output = item.endswith('.trjpk')

    return output

