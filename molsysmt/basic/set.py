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

    This function assigns new values to attributes in a molecular system. Values are set
    on specific elements (atoms, groups, etc.) and optionally for selected structures.
    The attributes to be modified are passed as keyword arguments.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to be modified. It can be in any of the :ref:`supported forms <Introduction_Forms>`.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, optional
        Level of elements on which the attribute values will be set. If not provided,
        the function will infer it from the attribute definitions.
    selection : str, tuple, list or numpy.ndarray, default='all'
        Selection of elements whose attributes will be modified. It can be a list/array
        of 0-based indices or a query string using one of the :ref:`supported selection syntaxes <Introduction_Selection>`.
        The default 'all' includes the entire system.
    structure_indices : str, tuple, list or numpy.ndarray, default='all'
        0-based indices of structures for which structural attributes will be modified. The default 'all' includes all
        structures.
    syntax : str, default='MolSysMT'
        Syntax used to interpret the `selection` string. See :ref:`Introduction_Selection` for details.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.
    **kwargs : dict
        Attributes to modify, passed as keyword arguments where the key is the attribute name
        and the value is the new value to be assigned.

    Raises
    ------
    NotSupportedFormError
        If the molecular system is provided in an unsupported form.
    ArgumentError
        If the input arguments do not meet the expected requirements.

    Notes
    -----
    - Supported molecular-system forms are described in :ref:`Introduction_Forms`.
    - Selection syntaxes and valid query expressions are described in :ref:`Introduction_Selection`.
    - If `element` is not specified, it is inferred from the attribute definition.
    - If the attribute runs over structures, `structure_indices` must be defined accordingly.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system.
    :func:`molsysmt.basic.get`
        Retrieving attribute values from a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert('181L')
    >>> msm.basic.get(molsys, element='group', selection='group_index==30', group_name=True)
    ['HIS']
    >>> msm.basic.set(molsys, selection='group_index==30', group_name='HSD')
    >>> msm.basic.get(molsys, element='group', selection='group_index==30', group_name=True)
    ['HSD']

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Set`

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

