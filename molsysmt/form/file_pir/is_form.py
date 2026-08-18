from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:pir.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form file:pir, False otherwise.
    """

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        output = item.endswith('.pir')

    return output
