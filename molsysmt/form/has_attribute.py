# If digest is used in this method, other methods become slower

def has_attribute(form, attribute):
    """
    Checking if a molecular systems'form has a certain attribute.

    The function returns True if the attribute is found in the molecular system's form, and False
    otherwise.


    Parameters
    ----------

    form : str, list or tuple of str
        Any of :ref:`the supported forms <Introduction_Forms>` by MolSysMT, or a list of them.

    attribute: str
        The attribute name to be checked in the molecular system.


    Returns
    -------
    bool
        The function returns a boolean value reporting whether or not the attribute is found in the
        molecular system.


    .. versionadded:: 0.8.3


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.


    See Also
    --------

    :func:`molsysmt.form.get_attributes`
        Getting the list of attributes of a molecular system's for's form.

    :func:`molsysmt.basic.get_attributes`
        Getting the list of attributes of a molecular system.

    :func:`molsysmt.basic.has_attribute`
        Checking if a molecular system has a certain attribute.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> msm.form.has_attribute('file:mmtf', 'box')
    True
    >>> msm.form.has_attribute('file:mmtf', 'forcefield')
    False
    >>> msm.form.has_attribute(['file:mmtf','molsysmt.MoleculeMechanicsDict'], 'forcefield')
    True


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Form > Has attribute <UTF_Has_attribute>`.


    """

    from . import _dict_modules

    if not isinstance(form, (list, tuple)):
        form = [form]

    output = False

    for aux_form in form:
        if attribute in _dict_modules[aux_form].attributes:
            if _dict_modules[aux_form].attributes[attribute]:
                return True

    return output

