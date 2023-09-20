from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np


@digest()
def set(molecular_system,
        element=None,
        selection='all',
        structure_indices='all',
        syntax='MolSysMT',
        **kwargs):
    """
    Setting attribute values to a molecular system.

    This function sets new values to attributes of a molecular system. The
    changed is done over the selection of elements and structure indices -if it
    is the case- specified through the input arguments. 

    Parameters
    ----------

    molecular_system : molecular system
        Molecular system, in any of :ref:`the supported forms
        <Introduction_Forms>`, to which the value of the attributes will be set by the function.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to which the value of the attributes will be set by the
        function. The selection can be given by a list, tuple or numpy array of
        element indices (0-based integers) -up to the value of the ``element``
        input argument-; or by means of a query string following any of
        :ref:`the selection syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : integer, tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) to be set when the attributes are structural.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).

    **kwargs : {{keyword : str,  value : any}, default None}
        The attributes to be changed are introduced as additional keywords together with the new values.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.

    ArgumentError
        The function raises an ArgumentError in case an input argument value
        does not meet the required conditions.

    SyntaxError
        The function raises a SyntaxError in case the syntax argument takes a not supported value. 


    .. versionadded:: 0.1.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system.

    :func:`molsysmt.basic.get`
        Getting attribute values from a molecular system.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> molecular_system = msm.convert('181L')
    >>> msm.basic.get(molecular_system, element='group', selection='group_index==30', group_name=True)
    'HIS'
    >>> msm.basic.set(molecular_system, selection='group_index==30', group_name='HSD')
    >>> msm.basic.get(molecular_system, element='group', selection='group_index==30', group_name=True)
    'HSD'


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Set <Tutorial_Set>`.


    """

    from . import select, where_is_attribute
    from molsysmt.attribute import attributes
    from molsysmt.form import _dict_modules

    value_of_in_attribute = {}
    for key in kwargs.keys():
        value_of_in_attribute[key] = kwargs[key]

    # selection

    in_attributes = value_of_in_attribute.keys()

    element_indices = {}

    if element is None:

        for in_attribute in in_attributes:
            if attributes[in_attribute]['runs_on_elements']:
                element = attributes[in_attribute]['set_to']
                if element not in element_indices:
                    if is_all(selection):
                        element_indices[element] = 'all'
                    else:
                        element_indices[element] = select(molecular_system, element=element, selection=selection,
                                                          syntax=syntax)

        for in_attribute in in_attributes:

            element = attributes[in_attribute]['set_to']

            dict_indices = {}
            if element != 'system':
                if attributes[in_attribute]['runs_on_elements']:
                    dict_indices['indices'] = element_indices[element]
            if attributes[in_attribute]['runs_on_structures']:
                dict_indices['structure_indices'] = structure_indices

            item, form = where_is_attribute(molecular_system, in_attribute, check_if_None=False)
            in_value = value_of_in_attribute[in_attribute]
            set_function = getattr(_dict_modules[form], f'set_{in_attribute}_to_{element}')
            set_function(item, **dict_indices, value=in_value)

    else:

        indices = None
        if element!='system':
            if is_all(selection):
                indices = 'all'
            else:
                indices = select(molecular_system, element=element, selection=selection, syntax=syntax)

        # doing the work here
        for in_attribute in in_attributes:

            dict_indices = {}
            if element != 'system':
                dict_indices['indices'] = indices
            if attributes[in_attribute]['runs_on_structures']:
                dict_indices['structure_indices'] = structure_indices

            item, form = where_is_attribute(molecular_system, in_attribute, check_if_None=False)
            in_value = value_of_in_attribute[in_attribute]
            set_function = getattr(_dict_modules[form], f'set_{in_attribute}_to_{element}')
            set_function(item, **dict_indices, value=in_value)

    pass

