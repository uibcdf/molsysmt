from molsysmt._private.digestion import digest

@digest()
def copy(molecular_system, output_filename=None, skip_digestion=False):
    """
    Making copies of molecular systems.

    This function makes an independent copy of a molecular system.


    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be duplicated by the function.

    output_filename : str
        Output file name in case the molecular system to be copied is a file.


    Returns
    -------

    Molecular system
        Molecular system copied from the molecular system introduced as input argument.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.

    ArgumentError
        The function raises an ArgumentError in case an input argument value
        does not meet the required conditions.


    .. versionadded:: 0.1.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = msm.basic.convert(demo['T4 lysozyme L99A']['181l.mmtf'])
    >>> molecular_system_2 = msm.basic.copy(molecular_system_1)
    >>> msm.basic.compare(molecular_system_1, molecular_system_2, rule='equal')
    True
    >>> id(molecular_system_1)==id(molecular_system_2)
    False


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Copy <Tutorial_Copy>`.


    """

    from . import get_form
    from molsysmt.form import is_file, _dict_modules

    form_in = get_form(molecular_system)

    if output_filename is None:

        if not isinstance(form_in, (list, tuple)):
            form_in = [form_in]
            molecular_system = [molecular_system]

        output = []

        for item_form, item in zip(form_in, molecular_system):
            output_item = _dict_modules[item_form].copy(item)
            output.append(output_item)

        if len(output)==1:
            output=output[0]

    else:

        output = _dict_modules[form_in].copy(molecular_system, output_filename=output_filename)

    return output

