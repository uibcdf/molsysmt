from molsysmt._private.digestion import digest, digest_output
from molsysmt._private.lists_and_tuples import is_list_or_tuple
from molsysmt.attribute.attributes import _required_indices


@digest
def get(molecular_system, element='system', indices=None, selection='all', structure_indices='all',
        syntaxis='MolSysMT', check=True, **kwargs):
    """get(item, element='system', indices=None, selection='all', structure_indices='all', syntaxis='MolSysMT')

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
       the selection syntaxis parsable by MolSysMT.

    syntaxis: str, default='MolSysMT'
       Selection syntaxis used in the argument `selection` (in case `selection` is a string). Find
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

    from .. import select, where_is_attribute
    from molsysmt.api_forms import dict_get

    arguments = []
    for key in kwargs.keys():
        if kwargs[key]:
            arguments.append(key)

    if not is_list_or_tuple(molecular_system):
        molecular_system = [molecular_system]

    if indices is None:
        if selection is not 'all':
            indices = select(molecular_system, element=element, selection=selection, syntaxis=syntaxis, check=False)
        else:
            indices = 'all'

    attributes = []

    for argument in arguments:

        dict_indices = {}
        if element != 'system':
            if 'indices' in _required_indices[argument]:
                dict_indices['indices'] = indices
        if 'structure_indices' in _required_indices[argument]:
            dict_indices['structure_indices'] = structure_indices

        aux_item, aux_form = where_is_attribute(molecular_system, argument, check=False)

        if aux_item is None:
            result = None
        else:
            result = dict_get[aux_form][element][argument](aux_item, **dict_indices)

        attributes.append(result)

    return digest_output(attributes)
