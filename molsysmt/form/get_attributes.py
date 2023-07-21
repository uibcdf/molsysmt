# If digest is used in this method, other methods become slower

def get_attributes(form, output_type='dictionary'):
    """
    Getting the list of attributes of a molecular system's form.

    The function returns a dictionary with all attribute names as keys and True or False as values
    reporting whether or not the attribute is in the molecular system's form.


    Parameters
    ----------

    form : str, list or tuple of str
        Any of :ref:`the supported forms <Introduction_Forms>` by MolSysMT, or a list of them.

    output_type : {'dictionary', 'list'}, default 'dictionary'

    Returns
    -------
    dict, list
        If ``output_type=='dictionary'`` a dictionary is returned with all
        attribute names as keys and booleans as values: True if the attribute
        is in the input molecular system's form, False otherwise.
        If ``output_type=='list'`` a list is returned with all
        attribute names in the molecular system's form.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.


    .. versionadded:: 0.8.3


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> dict_attributes = msm.form.get_attributes('file:mmtf')
    >>> dict_attributes['box']
    True
    >>> dict_attributes['forcefield']
    False
    >>> dict_attributes = msm.form.get_attributes(['file:mmtf','molsysmt.MolecularMechanicsDict'])
    >>> dict_attributes['box']
    True
    >>> dict_attributes['forcefield']
    True


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Form > Get attributes <UTF_Get_attributes>`.


    """

    from . import _dict_modules
    from molsysmt.attribute.attributes import attributes as _all_attributes

    if not isinstance(form, (list, tuple)):
        form = [form]

    output = {ii:False for ii in _all_attributes}

    for aux_form in form:
        for key, value in  _dict_modules[aux_form].attributes.items():
            if value:
                output[key]=value

    if output_type=='dictionary':
        return output
    elif output_type=='list':
        return [att for att in output if output[att]]

