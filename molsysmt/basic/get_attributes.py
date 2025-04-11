# If digest is used in this method, other methods become slower

def get_attributes(molecular_system, output_type='dictionary'):
    """
    Retrieve the list of attributes present in a molecular system.

    This function checks which attributes are available in the input molecular system and returns 
    either a dictionary indicating the presence (`True`/`False`) of each attribute or a list of 
    the attributes present, depending on the `output_type`.

    Parameters
    ----------
    molecular_system : molecular system
        The molecular system to be analyzed, in any of the :ref:`supported forms <Introduction_Forms>`.

    output_type : {'dictionary', 'list'}, default 'dictionary'
        Format of the returned result. If 'dictionary', returns all supported attributes as keys
        with boolean values indicating presence. If 'list', returns only the present attribute names.

    Returns
    -------
    dict or list
        - If `output_type == 'dictionary'`: a dictionary with attribute names as keys and booleans as values.
        - If `output_type == 'list'`: a list with the names of attributes present in the molecular system.

    Raises
    ------
    NotSupportedFormError
        If the input molecular system has an unsupported form.

    Notes
    -----
    See :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>` for a list of supported input forms.

    See Also
    --------
    :func:`molsysmt.basic.has_attribute`
        Check whether a specific attribute exists in a molecular system.

    :func:`molsysmt.basic.get_form`
        Retrieve the form of a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.mmtf'])
    >>> attributes = msm.get_attributes(molsys)
    >>> attributes['box']
    True
    >>> attributes['forcefield']
    False
    >>> msm.get_attributes(molsys, output_type='list')
    ['coordinates', 'box', 'time', ...]

    .. admonition:: User guide

       For a tutorial on how to use this function, see:
       :ref:`User Guide > Tools > Basic > Get attributes <Tutorial_Get_attributes>`

    .. versionadded:: 1.0.0
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
                if _dict_modules[form_in].has_attribute(item, key, skip_digestion=True):
                    output[key]=value

    if output_type=='dictionary':
        return output
    elif output_type=='list':
        return [att for att in output if output[att]]

