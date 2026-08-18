
def is_form(item):
    """
    Checking whether an item is an instance of form openmm.GromacsTopFile.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form openmm.GromacsTopFile, False otherwise.
    """
    from openmm.app import GromacsTopFile

    return isinstance(item, GromacsTopFile)
