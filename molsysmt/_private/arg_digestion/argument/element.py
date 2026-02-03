from molsysmt._private.exceptions import ArgumentError

def digest_element(element, caller=None):
    """ Checks if a syntax has the correct type and value

        Parameters
        ----------
        element : str
            The name of the element.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        ArgumentError
            A ArgumentError is raised if the element is not a string or its name is not valid.

    """

    from molsysmt.element import _elements, _plural_elements_to_singular

    if isinstance(element, str):
        element_name_lower = element.lower()
        if element_name_lower in _plural_elements_to_singular:
            return _plural_elements_to_singular[element_name_lower]
        if element_name_lower in _elements:
            return element_name_lower
    elif element is None:
        if caller=='molsysmt.basic.set.set':
            return element

    raise ArgumentError('element', value=element, caller=caller, message=None)

