from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:psf.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form file:psf, False otherwise.
    """

    output = False

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        if item.endswith('.psf'):
            output = True

    return output

