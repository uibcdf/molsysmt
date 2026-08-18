from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:psf.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    .. versionadded:: 1.0.0
    """

    output = False

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        if item.endswith('.psf'):
            output = True

    return output

