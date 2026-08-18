def is_form(item):
    """
    Checking whether an item is an instance of form MDAnalysis.AtomGroup.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form MDAnalysis.AtomGroup, False otherwise.
    """

    output = False

    class_name = str(type(item))
    if 'MDAnalysis.core.groups.AtomGroup' in class_name:
        output = True

    return output
