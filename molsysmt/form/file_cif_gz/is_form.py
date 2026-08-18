from pathlib import PosixPath

def is_form(item):
    """
    Checking whether an item is an instance of form file:cif.gz.

    Parameters
    ----------
    item : file:cif.gz
        Source item in file:cif.gz form.

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
        output = item.endswith('.cif.gz')

    return output

