def is_element(element):
    """
    Checking if a string represents a valid structural element level in MolSysMT.

    Parameters
    ----------
    element : str
        String to test.

    Returns
    -------
    bool
        True if element is in ('atom', 'group', 'component', 'molecule', 'chain', 'entity', 'bond'), False otherwise.

    .. versionadded:: 1.0.0
    """

    from molsysmt.element import _elements, _plural_elements_to_singular

    output = False

    if element in _plural_elements_to_singular:
        output = True

    elif element in _elements:
        output = True

    return output
