
def is_form(item):
    """
    Checking whether an item is an instance of form MDAnalysis.Universe.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item in MDAnalysis.Universe form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'MDAnalysis.core.universe.Universe')
    return output

