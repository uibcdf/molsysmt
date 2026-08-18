
def is_form(item):
    """
    Checking whether an item is an instance of form pytraj.Trajectory.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form pytraj.Trajectory, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'pytraj.trajectory.trajectory.Trajectory')

    return output

