from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get(molecular_system,
        element='system',
        selection='all',
        structure_indices='all',
        mask=None,
        syntax='MolSysMT',
        get_missing_bonds=True,
        output_type='values',
        skip_digestion=False,
        **kwargs):
    """
    Retrieving attribute values from a molecular system.

    This function retrieves values of one or more attributes from a molecular system (or from
    a selected subset of it), optionally specifying the hierarchical `element` level. Attributes
    to be returned are indicated via keyword flags in `**kwargs` (e.g., ``n_atoms=True``,
    ``coordinates=True``).

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to query, in any of the :ref:`supported forms <Introduction_Forms>`.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'bond', 'system'}, default 'system'
        Element level at which attributes are retrieved.
    selection : int, tuple, list, numpy.ndarray or str, default 'all'
        Subset of elements (interpreted at the level set by `element`) to use when retrieving
        attributes. Either a 0-based index collection or a selection string parsed according to
        :ref:`Introduction_Selection`.
    structure_indices : int, tuple, list, numpy.ndarray or 'all', default 'all'
        0-based indices of structures to include in the query. Required for structural attributes (e.g., coordinates, box, time).
    mask : array-like of bool, optional
        Boolean mask to apply after selection and structure filtering. Must match the shape of the selected elements.
    syntax : str, default 'MolSysMT'
        Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
    get_missing_bonds : bool, default False
        Whether to infer and return bond information on the fly when bond-related attributes
        are requested and the input form lacks explicit connectivity. The inference uses the
        form backend’s heuristics (distance/chemistry-aware thresholds).
    output_type : {'values', 'dictionary'}, default 'values'
        Output format:
        - ``value` — **convenience mode**:
          * if exactly **one** attribute is requested, return its value directly;
          * if **multiple** attributes are requested, return a **tuple** of values following
            the order in which the attributes were provided in `**kwargs`.
        - ``'dictionary'`` — return a dictionary mapping attribute names to values.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent
    **kwargs
        Attribute flags selecting which values to retrieve (e.g., ``n_atoms=True``,
        ``coordinates=True``, ``time=True``, ``box=True``, etc.). Only attributes flagged
        as `True` are returned.

    Returns
    -------
    Any or tuple or dict or None
        Depending on `output_type`:
        - If ``output_type == 'values'`` and a single attribute is requested: the attribute value. This value can be
        `None` if the attribute is not found in the system.
        - If ``output_type == 'values'`` and multiple attributes are requested: a tuple with values
          in the order given by `**kwargs`.
        - If ``output_type == 'dictionary'``: a dictionary ``{attribute_name: value}``.

    Raises
    ------
    NotSupportedFormError
        If the molecular system has an unsupported form.
    ArgumentError
        If any input argument is invalid or inconsistent.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.
    :func:`molsysmt.basic.get_attributes`
        Get the list of available attributes for a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.get(molsys, element='group', selection=[10,11,12], n_atoms=True)
    [9, 4, 8]
    >>> msm.get(molsys, element='molecule', selection='molecule_type=="water"', n_molecules=True)
    136
    >>> msm.get(molsys, element='bond', selection=[0,1,2,3,4], bonded_atoms=True)
    [0, 1, 2, 3, 4, 8]


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Get`.


    .. versionadded:: 1.0.0
    """

    from .. import select, where_is_attribute, get_form, convert
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes, bonds_are_required_to_get_attribute
    from molsysmt.attribute import is_topological_attribute, is_structural_attribute

    form = get_form(molecular_system)

    if isinstance(form, (list, tuple)):
        attributes_filter = _dict_modules[form[0]].attributes.copy()
        for aux_form in form[1:]:
            for aux_attribute, aux_bool in _dict_modules[aux_form].attributes.items():
                if aux_bool:
                    attributes_filter[aux_attribute]=True
    else:
        attributes_filter = _dict_modules[form].attributes

    in_attributes = []
    for key in kwargs.keys():
        if kwargs[key]:
            in_attributes.append(key)

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]
        form = [form]

    # Correction from element='system' to element='atom' if:
    #   selection is not 'all' or indices is not None
    #   all attributes are attributable to atoms

    if (element=='system') and (not is_all(selection)):

        from molsysmt.attribute import attributes as _attributes

        attributes_from_atom = []
        attributes_from_system = []
        for ii in in_attributes:
            if 'atom' in _attributes[ii]['get_from']:
                attributes_from_atom.append(ii)
            elif 'system' in _attributes[ii]['get_from']:
                attributes_from_system.append(ii)

        aux_result_atoms = {}
        aux_result_system = {}

        if len(attributes_from_atom) > 0:
            aux_result_atoms = get(molecular_system, element='atom', selection=selection,
                                    structure_indices=structure_indices, mask=mask, syntax=syntax,
                                    get_missing_bonds=get_missing_bonds, output_type='dictionary',
                                    skip_digestion=True, **{ii:True for ii in attributes_from_atom})

        if len(attributes_from_system) > 0:
            aux_result_system = get(molecular_system, element='system', selection='all',
                                    structure_indices=structure_indices,
                                    get_missing_bonds=get_missing_bonds, output_type='dictionary',
                                    skip_digestion=True, **{ii:True for ii in attributes_from_system})

        aux_result = aux_result_atoms | aux_result_system

        output = []
        for ii in in_attributes:
            output.append(aux_result[ii])

        if output_type=='values':
            if len(output) == 1:
                return output[0]
            else:
                return output
        elif output_type=='dictionary':
            return dict(zip(in_attributes, output))

    if not is_all(selection):
        indices = select(molecular_system, element=element, selection=selection, mask=mask, syntax=syntax, skip_digestion=True)
    else:
        if (mask is None) or (is_all(mask)):
            indices = 'all'
        else:
            indices = select(molecular_system, element=element, selection=mask, syntax=syntax, skip_digestion=True)

    piped_molecular_systems, piped_attributes = _piped_molecular_system(molecular_system, element, in_attributes)

    if piped_molecular_systems is None:

        output = []

        for in_attribute in in_attributes:

            if attributes_filter[in_attribute]:

                dict_indices = {}
                if element != 'system':
                    if attributes[in_attribute]['runs_on_elements']:
                        dict_indices['indices'] = indices
                if attributes[in_attribute]['runs_on_structures']:
                    dict_indices['structure_indices'] = structure_indices

                aux_item, aux_form = where_is_attribute(molecular_system, in_attribute, skip_digestion=True)

                if aux_item is None:
                    result = None
                else:
                    aux_get = getattr(_dict_modules[aux_form], f'get_{in_attribute}_from_{element}')
                    result = aux_get(aux_item, **dict_indices)

            else:

                result = None

            output.append(result)

    else:

        output_dictionary = {}

        for aux_molecular_system, aux_attributes in zip(piped_molecular_systems, piped_attributes):

            if aux_molecular_system is None:
                aux_molecular_system = molecular_system

            aux_dict = get(aux_molecular_system, element=element, selection=indices,
                           structure_indices=structure_indices, mask=mask, syntax=syntax,
                           get_missing_bonds=get_missing_bonds, output_type='dictionary', skip_digestion=False,
                           **{ii:True for ii in aux_attributes})

            output_dictionary.update(aux_dict)

        output = []

        for in_attribute in in_attributes:

            output.append(output_dictionary[in_attribute])

    if output_type=='values':
        if len(output) == 1:
            return output[0]
        else:
            return output
    elif output_type=='dictionary':
        return dict(zip(in_attributes, output))
        

def _piped_molecular_system(molecular_system, element, in_attributes):


    from .. import select, where_is_attribute, get_form, convert
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes, bonds_are_required_to_get_attribute
    from molsysmt.attribute import is_topological_attribute, is_structural_attribute

    topological_pipes = {}
    structural_pipes = {}
    any_pipes = {}

    form = get_form(molecular_system)

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]
        form = [form]

    for aux_form in form:
        topological_pipes[aux_form] = getattr(_dict_modules[aux_form], f'piped_topological_attribute')
        structural_pipes[aux_form] = getattr(_dict_modules[aux_form], f'piped_structural_attribute')
        any_pipes[aux_form] = getattr(_dict_modules[aux_form], f'piped_any_attribute')

    not_piped = all([ii is None for ii in topological_pipes.values()]) & \
                all([ii is None for ii in structural_pipes.values()]) & \
                all([ii is None for ii in any_pipes.values()])  

    if not_piped or len(in_attributes)==1:

        return None, None

    else:

        aux_topological_attributes = []
        aux_topological_pipes = []
        aux_structural_attributes = []
        aux_structural_pipes = []
        aux_any_pipes = []

        bonds_required_by_attributes = False

        for in_attribute in in_attributes:
            bonds_required_by_attributes += bonds_are_required_to_get_attribute(in_attribute, element,
                                                                                skip_digestion=True)
            if is_topological_attribute(in_attribute, skip_digestion=True):
                aux_topological_attributes.append(in_attribute)
                _, aux_form = where_is_attribute(molecular_system, in_attribute, skip_digestion=True)
                if aux_form is not None:
                    if topological_pipes[aux_form] is not None:
                        if topological_pipes[aux_form] not in aux_topological_pipes:
                            aux_topological_pipes.append(topological_pipes[aux_form])
                    if any_pipes[aux_form] is not None:
                        if any_pipes[aux_form] not in aux_any_pipes:
                            aux_any_pipes.append(any_pipes[aux_form])
            elif is_structural_attribute(in_attribute, skip_digestion=True):
                _, aux_form = where_is_attribute(molecular_system, in_attribute)
                aux_structural_attributes.append(in_attribute)
                if aux_form is not None:
                    if structural_pipes[aux_form] is not None:
                        if structural_pipes[aux_form] not in aux_structural_pipes:
                            aux_structural_pipes.append(structural_pipes[aux_form])
                    if any_pipes[aux_form] is not None:
                        if any_pipes[aux_form] not in aux_any_pipes:
                            aux_any_pipes.append(any_pipes[aux_form])

        n_top_pipes = len(aux_topological_pipes)
        n_str_pipes = len(aux_structural_pipes)
        n_any_pipes = len(aux_any_pipes)

        n_top_atts = len(aux_topological_attributes)
        n_str_atts = len(aux_structural_attributes)

        output_systems = []
        output_attributes = []

        if n_top_pipes==0 and n_str_pipes==0 and n_any_pipes==0:

            output_systems = None
            output_attributes = None

        elif n_top_atts>0 and n_str_atts==0:

            if n_top_pipes==1:

                aux_molecular_system = convert(molecular_system, to_form=aux_topological_pipes[0],
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

            else:

                aux_molecular_system = convert(molecular_system, to_form='molsysmt.Topology',
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

            output_systems.append(aux_molecular_system)
            output_attributes.append(aux_topological_attributes)

        elif n_top_atts==0 and n_str_atts>0:

            if n_str_pipes == 1:

                aux_molecular_system = convert(molecular_system, to_form=aux_structural_pipes[0],
                                               skip_digestion=True)

            else:

                aux_molecular_system = convert(molecular_system, to_form='molsysmt.Structures', skip_digestion=True)

            output_systems.append(aux_molecular_system)
            output_attributes.append(aux_structural_attributes)

        else:

            if n_any_pipes == 1:

                aux_molecular_system = convert(molecular_system, to_form=aux_any_pipes[0],
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_topological_attributes+aux_structural_attributes)

            elif n_any_pipes > 1:

                aux_molecular_system = convert(molecular_system, to_form='molsysmt.MolSys',
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_topological_attributes+aux_structural_attributes)

            elif n_any_pipes == 0:

                if n_top_pipes == 1:

                    aux_molecular_system = convert(molecular_system, to_form=aux_topological_pipes[0],
                                                   get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                elif n_top_pipes > 1:

                    aux_molecular_system = convert(molecular_system, to_form='molsysmt.Topology',
                                                   get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

                else:

                    aux_molecular_system = None

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_topological_attributes)

                if n_str_pipes == 1:

                    aux_molecular_system = convert(molecular_system, to_form=aux_structural_pipes[0],
                                                   skip_digestion=True)

                elif n_str_pipes > 1:

                    aux_molecular_system = convert(molecular_system, to_form='molsysmt.Structures', skip_digestion=True)

                else:

                    aux_molecular_system = None

                output_systems.append(aux_molecular_system)
                output_attributes.append(aux_structural_attributes)

    return output_systems, output_attributes

