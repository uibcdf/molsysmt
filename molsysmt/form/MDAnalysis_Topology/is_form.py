def is_form(item):
    """
    Checking whether an item is an instance of form MDAnalysis.Topology.

    Parameters
    ----------
    item : MDAnalysis.Topology
        Source item in MDAnalysis.Topology form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'MDAnalysis.core.topology.Topology')

    return output

