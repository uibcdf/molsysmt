def is_form(item):
    """
    Checking whether an item is an instance of form openff.Topology.

    Parameters
    ----------
    item : openff.Topology
        Source item in openff.Topology form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    class_module = type(item).__module__
    class_name = type(item).__name__

    return 'openff.toolkit' in class_module and class_name == 'Topology'
