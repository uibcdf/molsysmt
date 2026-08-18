def is_form(item):
    """
    Checking whether an item is an instance of form openff.Molecule.


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

    class_module = type(item).__module__
    class_name = type(item).__name__

    return 'openff.toolkit' in class_module and class_name == 'Molecule'
