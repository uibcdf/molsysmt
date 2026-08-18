def is_form(item):
    """
    Checking whether an item is an instance of form MDAnalysis.AtomGroup.


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

    class_name = str(type(item))
    if 'MDAnalysis.core.groups.AtomGroup' in class_name:
        output = True

    return output
