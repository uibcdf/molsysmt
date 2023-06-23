# If digest is used in this method, other methods become slower

def has_attribute(molecular_system, attribute):
    """
    Checking if a molecular system has a certain attribute.

    The function returns True if the attribute is found in the molecular system, and False
    otherwise.


    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by the function.

    attribute: str
        The attribute name to be checked in the molecular system.


    Returns
    -------
    bool
        The function returns a boolean value reporting whether or not the attribute is found in the
        molecular system.


    .. versionadded:: 0.1.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.


    See Also
    --------

    :func:`molsysmt.basic.get_attributes`
        Getting the list of attributes of a molecular system.

    :func:`molsysmt.basic.get`
        Getting attribute values from a molecular system.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.basic.has_attribute(molecular_system, 'box')
    True
    >>> msm.basic.has_attribute(molecular_system, 'forcefield')
    False


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Has attribute <Tutorial_Has_attribute>`.


    """

    from molsysmt import get_form
    from molsysmt.form import _dict_modules

    forms_in = get_form(molecular_system)

    if not isinstance(forms_in, (list, tuple)):
        forms_in = [forms_in]
        molecular_system = [molecular_system]

    output = False

    for form_in, item in zip(forms_in, molecular_system):
        if _dict_modules[form_in].has_attribute(item, attribute):
            output=True
            break

    return output

