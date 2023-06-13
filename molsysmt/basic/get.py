from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all


@digest()
def get(molecular_system,
        element='system',
        indices=None,
        selection='all',
        structure_indices='all',
        mask=None,
        syntax='MolSysMT',
        output_type='values',
        **kwargs):
    """get(item, element='system', indices=None, selection='all', structure_indices='all', syntax='MolSysMT')

    Get specific attributes and observables.

    Paragraph with detailed explanation.

    Parameters
    ----------

    molecular_system: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    element: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of elementted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    selection: str, list, tuple or np.ndarray, default='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT.

    structure_indices : nt, list, tuple or np.ndarray, default=None

    syntax: str, default='MolSysMT'
       Selection syntax used in the argument `selection` (in case `selection` is a string). Find
       current options supported by MolSysMt in section 'Selection'.

    Returns
    -------
    Attributes
        Returns the specified attribute. If more than one attribute is selected, it returns a list
        with all the specified attributes.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`

    Notes
    -----

    """

    from .. import select, where_is_attribute, get_form, convert
    from molsysmt.form import _dict_modules
    from molsysmt.attribute import attributes

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

    if indices is None:
        if not is_all(selection):
            indices = select(molecular_system, element=element, selection=selection, mask=mask, syntax=syntax)
        else:
            if (mask is None) or (is_all(mask)):
                indices = 'all'
            else:
                indices = select(molecular_system, element=element, selection=mask, syntax=syntax)

    output = []

    for in_attribute in in_attributes:

        if attributes_filter[in_attribute]:

            dict_indices = {}
            if element != 'system':
                if attributes[in_attribute]['runs_on_elements']:
                    dict_indices['indices'] = indices
            if attributes[in_attribute]['runs_on_structures']:
                dict_indices['structure_indices'] = structure_indices

            aux_item, aux_form = where_is_attribute(molecular_system, in_attribute)

            if aux_item is None:
                result = None
            else:
                aux_get = getattr(_dict_modules[aux_form], f'get_{in_attribute}_from_{element}')
                result = aux_get(aux_item, **dict_indices)

        else:

            result = None

        output.append(result)

    if output_type=='values':
        if len(output) == 1:
            return output[0]
        else:
            return output
    elif output_type=='dictionary':
        return dict(zip(in_attributes, output))

