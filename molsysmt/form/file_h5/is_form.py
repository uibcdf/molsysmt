from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:h5.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form file:h5, False otherwise.
    """

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        if item.endswith('.h5') or item.endswith('.hdf5'):
            output = True

    return output

