def is_component_type(component_type):
    """
    Checking if a string represents a valid recognized component type in MolSysMT.




    Parameters
    ----------
    component_type : object
        Argument component_type.

    Returns
    -------
    bool
        True if recognized component type, False otherwise.




    .. versionadded:: 1.0.0
    """

    from molsysmt.element.component import _component_types
    from molsysmt.element.component import _plural_component_types_to_singular

    output = False

    if component_type in _component_types:
        output = True

    elif component_type in _plural_component_types_to_singular:
        output = True

    return output

