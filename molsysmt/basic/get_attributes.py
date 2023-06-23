# If digest is used in this method, other methods become slower

def get_attributes(molecular_system, output_type='dictionary'):
    """
    Getting the list of attributes of a molecular system.

    The function returns a dictionary with all attribute names as keys and True or False as values
    reporting whether or not the attribute is in the input molecular system.


    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be checked by the function.

    output_type : {'dictionary', 'list'}, default 'dictionary'

    Returns
    -------
    dict, list
        If ``output_type=='dictionary'`` a dictionary is returned with all
        attribute names as keys and booleans as values: True if the attribute
        is found in the molecular system, False otherwise.
        If ``output_type=='list'`` a list is returned with all
        attribute names in the molecular system.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.


    .. versionadded:: 0.5.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system = msm.basic.convert(demo['T4 lysozyme L99A']['181l.mmtf'])
    >>> dict_attributes = msm.basic.get_attributes(molecular_system)
    >>> dict_attributes['box']
    True
    >>> dict_attributes['forcefield']
    False


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Get attributes <Tutorial_Get_attributes>`.


    """

    from . import get_form
    from molsysmt.form import _dict_modules
    from molsysmt.attribute.attributes import attributes as _all_attributes

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    output = {ii:False for ii in _all_attributes}

    for form_in, item in zip(forms_in, molecular_system):
        for key, value in  _dict_modules[form_in].attributes.items():
            if value:
                output[key]=value

    if output_type=='dictionary':
        return output
    elif output_type=='list':
        return [att for att in output if output[att]]

