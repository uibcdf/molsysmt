def is_form(item):
    """
    Checking whether an item is an instance of form mdtraj.Topology.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form mdtraj.Topology, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mdtraj.core.topology.Topology')

    return output

