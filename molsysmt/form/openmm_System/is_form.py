def is_form(item):
    """
    Checking whether an item is an instance of form openmm.System.

    Parameters
    ----------
    item : openmm.System
        Source item in openmm.System form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'openmm.openmm.System')

    return output

