from molysmt._private.exceptions import ArgumentError
from molsysmt.element.elements import elements, elements_from_plural

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

    if isinstance(element, str):
        element_name_lower = element.lower()
        if element_name_lower in elements_from_plural:
            return elements_from_plural[element_name_lower]
        if element_name_lower in elements:
            return element_name_lower

    raise ArgumentError('element', caller=caller, message=None)

