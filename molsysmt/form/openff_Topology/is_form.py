def is_form(item):
    """
    Checking whether an item is an instance of form openff.Topology.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form openff.Topology, False otherwise.
    """

    class_module = type(item).__module__
    class_name = type(item).__name__

    return 'openff.toolkit' in class_module and class_name == 'Topology'
