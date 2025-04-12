from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np


@digest()
def set(molecular_system,
        element=None,
        selection='all',
        structure_indices='all',
        syntax='MolSysMT',
        skip_digestion=False,
        **kwargs):
    """
    Setting attribute values in a molecular system.

    This function assigns new values to attributes of a molecular system. The change is applied to
    the selected elements and, if applicable, to specific structures, as specified by the
    `selection` and `structure_indices` arguments.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of the :ref:`supported forms <Introduction_Forms>`, whose
        attributes will be updated.

    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, optional
        Level of elements to which the attribute values will be set. Required for attributes that
        depend on a specific element level.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements whose attributes will be modified. The selection can be given by a
        list, tuple or NumPy array of 0-based indices; or as a query string using one of the
        :ref:`supported selection syntaxes <Introduction_Selection>`.

    structure_indices : index, tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) to which the structural attributes will be set.

    syntax : str, default 'MolSysMT'
        Selection syntax used to interpret the `selection` string.

    **kwargs : dict
        Attributes to modify, passed as keyword arguments where the key is the attribute name and the
        value is the new value to be set.

    Raises
    ------
    NotSupportedFormError
        Raised if the molecular system is provided in an unsupported form.

    ArgumentError
        Raised if the input arguments do not meet the expected requirements.

    Notes
    -----
    The list of supported molecular system forms is described in:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    For supported selection syntaxes and usage examples, see:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system.

    :func:`molsysmt.basic.get`
        Retrieving attribute values from a molecular system.

    Examples
    --------
    The following example illustrates how to change the name of a group in a protein:

    >>> import molsysmt as msm
    >>> molsys = msm.convert('181L')
    >>> msm.basic.get(molsys, element='group', selection='group_index==30', group_name=True)
    'HIS'
    >>> msm.basic.set(molsys, selection='group_index==30', group_name='HSD')
    >>> msm.basic.get(molsys, element='group', selection='group_index==30', group_name=True)
    'HSD'

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Set <Tutorial_Set>`

    .. versionadded:: 1.0.0

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

