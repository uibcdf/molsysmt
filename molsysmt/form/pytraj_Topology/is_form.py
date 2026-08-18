
def is_form(item):
    """
    Checking whether an item is an instance of form pytraj.Topology.


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

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'pytraj.topology.topology.Topology')

    return output

