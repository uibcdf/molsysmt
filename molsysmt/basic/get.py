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
    Getting attribute values from a molecular system.

    Molecular systems are defined by their attributes and the attributes of
    their elements. This function retrieves the value of the required set of
    attributes given a selection of elements and structures. If the form of the
    input molecular system do not have the attribute required, a None is returned.

    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by the function.

    element: {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'system'
        The values obtained for the required attributes correspond to the
        elements specified by this argument.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to be analysed by the
        function. The selection can be given by a list, tuple or numpy array of
        element indices (0-based integers) -up to the value of the ``element``
        input argument-; or by means of a query string following any of
        :ref:`the selection syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : integer, tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) to be analysed when the attributes are structural.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).

    output_type: {'values', 'dictionary'}, default 'values'
        If 'values', the list of attribute values are returned in the same
        order they were required. With 'dictionary' a dictionary is returned
        with the attribute names as keys, and corresponding attribute values as
        values.

    **kwargs : {{keyword : str,  value : bool}, default None}
        The attributes required are introduced as additional keywords with value 'True'
        if their value needs to be extracted.


    Returns
    -------
    Attribute values, dict
        The function returns the required attribute values as a list if the
        input argument ``output_type`` takes the value 'values'; or together
        with the attribute names in a dictionary if the argument
        ``output_type`` takes the value 'dictionary'. If a required attribute
        is not found in the form of the input molecular system, the
        function assigns None as returned value.


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
        Selecting elements of a molecular system


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.basic.get(molecular_system, element='group', selection=[10,11,12], n_atoms=True)
    [9, 6, 8]
    >>> msm.get(molecular_system, element='molecule', selection='molecule_type=="water"', n_molecules=True)
    165
    >>> msm.get(molecular_system, element='bond', selection=[0,1,2,3,4], bonded_atoms=True)
    array([[0, 1],
           [1, 2],
           [2, 3],
           [1, 4],
           [4, 5]])


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Get <Tutorial_Get>`.


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

        all_attributes_from_atom = np.all(['atom' in _attributes[ii]['get_from'] for ii in in_attributes])

        if all_attributes_from_atom:
            element = 'atom'

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

            aux_dict = get(aux_molecular_system, element=element, selection=selection,
                           structure_indices=structure_indices, mask=mask, syntax=syntax,
                           get_missing_bonds=get_missing_bonds, output_type='dictionary', skip_digestion=True,
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
                        if any_attribute[aux_form] not in aux_any_pipes:
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

                aux_molecular_system = convert(molecular_system, to_form=aux_piped_any_attribute[0],
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

            elif n_any_pipes > 1:

                aux_molecular_system = convert(molecular_system, to_form='molsysmt.MolSys',
                                               get_missing_bonds=bonds_required_by_attributes, skip_digestion=True)

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

