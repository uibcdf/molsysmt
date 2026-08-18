def is_component_type(component_type):
    """
    Checking if a string represents a valid recognized component type in MolSysMT.

    Parameters
    ----------
    component_type : str
        String to test.

    Returns
    -------
    bool
        True if recognized component type, False otherwise.

    .. versionadded:: 1.0.0
    """
    from molsysmt.element.component import _component_types
    return component_type in _component_types
