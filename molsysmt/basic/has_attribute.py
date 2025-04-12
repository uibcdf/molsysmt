# If digest is used in this method, other methods become slower

def has_attribute(molecular_system, attribute):
    """
    Check whether a molecular system has a specific attribute.

    This function returns `True` if the given attribute is present in the input molecular system,
    and `False` otherwise. The presence of attributes depends on the form of the molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        The molecular system to be analyzed, in any of the :ref:`supported forms <Introduction_Forms>`.

    attribute : str
        Name of the attribute to check.

    Returns
    -------
    bool
        `True` if the attribute is available in the molecular system, `False` otherwise.

    Raises
    ------
    NotSupportedFormError
        If the molecular system has a form that is not supported.

    Notes
    -----
    For a complete list of supported forms and their corresponding attributes, see:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    See Also
    --------
    :func:`molsysmt.basic.get_attributes`
        Retrieve the list of attributes available in a molecular system.

    :func:`molsysmt.basic.get`
        Retrieve values of specific attributes from a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = msm.convert(systems['T4 lysozyme L99A']['181l.mmtf'])
    >>> msm.has_attribute(molsys, 'box')
    True
    >>> msm.has_attribute(molsys, 'forcefield')
    False

    .. admonition:: User guide

       For a tutorial on using this function, see:
       :ref:`User Guide > Tools > Basic > Has attribute <Tutorial_Has_attribute>`

    .. versionadded:: 1.0.0
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

