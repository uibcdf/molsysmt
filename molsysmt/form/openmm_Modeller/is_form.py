
def is_form(item):
    """
    Checking whether an item is an instance of form openmm.Modeller.

    Parameters
    ----------
    item : openmm.Modeller
        Source item in openmm.Modeller form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'openmm.app.modeller.Modeller')

    return output

