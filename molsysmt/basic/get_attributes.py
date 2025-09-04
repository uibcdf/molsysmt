from molsysmt._private.digestion import digest


@digest()
def get_attributes(molecular_system, include_none=False, output_type='dictionary', skip_digestion=False):
    """
    Retrieving available attributes from a molecular system.

    This function inspects the input molecular system and reports which attributes are available
    according to MolSysMT’s attribute registry. The result can be returned either as a dictionary
    mapping attribute names to booleans or as a list containing only the present attributes.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyze, in any of the :ref:`supported forms <Introduction_Forms>`.
    include_none : bool, default False
        Whether to consider attributes with value `None` as present when probing availability.
        If `True`, attributes that exist but currently hold `None` will be marked as present.
    output_type : {'dictionary', 'list'}, default 'dictionary'
        Format of the returned result. If ``'dictionary'``, returns all supported attributes as
        keys with boolean values indicating presence. If ``'list'``, returns only the names of
        attributes present in the molecular system.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.


    Returns
    -------
    dict or list
        If ``output_type == 'dictionary'``: dictionary with attribute names as keys and
        booleans as values indicating availability. If ``output_type == 'list'``: list with the names of attributes
        present.


    Raises
    ------
    NotSupportedFormError
        If the input molecular system has an unsupported form.
    ArgumentError
        If input arguments are invalid or inconsistent.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.has_attribute`
        Check whether a specific attribute exists in a molecular system.
    :func:`molsysmt.basic.get_form`
        Retrieve the form of a molecular system.
    :func:`molsysmt.basic.get` :
        Retrieve attribute values from a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> attributes = msm.get_attributes(molsys)
    >>> attributes['box']
    True
    >>> attributes['forcefield']
    False
    >>> output = msm.get_attributes(molsys, output_type='list')
    >>> isinstance(output, list)
    True
    >>> 'molecule_id' in output
    True
    >>> 'forcefield' in output
    False

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Get_attributes`.

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
                if _dict_modules[form_in].has_attribute(item, key, include_none=include_none, skip_digestion=True):
                    output[key]=value

    if output_type=='dictionary':
        return output
    elif output_type=='list':
        return [att for att in output if output[att]]

