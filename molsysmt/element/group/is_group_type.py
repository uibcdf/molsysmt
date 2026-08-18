def is_group_type(group_type):
    """
    Checking if a string represents a valid, recognized group type in MolSysMT.

    Parameters
    ----------
    group_type : str
        String to test.

    Returns
    -------
    bool
        True if recognized group type, False otherwise.

    .. versionadded:: 1.0.0
    """
    from molsysmt.element.group import _group_types
    return group_type in _group_types
