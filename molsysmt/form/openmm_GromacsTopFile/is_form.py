
def is_form(item):
    """
    Checking whether an item is an instance of form openmm.GromacsTopFile.


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
    from openmm.app import GromacsTopFile

    return isinstance(item, GromacsTopFile)
