from molsysmt._private.digestion import digest

@digest()
def copy(molecular_system, output_filename=None, skip_digestion=False):
    """
    Create an independent copy of a molecular system.

    This function returns a deep copy of the input molecular system, ensuring the result is fully 
    detached and independent from the original. If the input is a file, a copy can optionally be 
    written to a new file using the `output_filename` argument.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to be duplicated, in any of the :ref:`supported forms <Introduction_Forms>`.

    output_filename : str, optional
        Name of the output file to write, in case the molecular system is in file form. If not provided,
        the copied file remains in memory or uses a temporary filename.

    skip_digestion : bool, default False
        If True, skip digestion and validation of the input system before copying.

    Returns
    -------
    molecular_system : molecular system
        A new molecular system, independent of the original.

    Raises
    ------
    NotSupportedFormError
        If the input molecular system has a form that is not supported.

    ArgumentError
        If the input arguments are invalid or inconsistent.

    Notes
    -----
    See :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>` for a list of supported forms.

    See Also
    --------
    :func:`molsysmt.basic.convert`
        Convert a molecular system into another form.

    :func:`molsysmt.basic.compare`
        Compare two molecular systems to check for identity or equality.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys_A = msm.convert(msm.systems['T4 lysozyme L99A']['181l.mmtf'])
    >>> molsys_B = msm.copy(molsys_A)
    >>> msm.compare(molsys_A, molsys_B, rule='equal')
    True
    >>> id(molsys_A) == id(molsys_B)
    False

    .. admonition:: User guide

       For a tutorial on using this function, see:
       :ref:`User Guide > Tools > Basic > Copy <Tutorial_Copy>`

    .. versionadded:: 1.0.0
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

