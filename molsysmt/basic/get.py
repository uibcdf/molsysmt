from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt.attribute.attributes import _required_indices


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

    from .. import select, where_is_attribute
    from molsysmt.api_forms import dict_get

    arguments = []
    for key in kwargs.keys():
        if kwargs[key]:
            arguments.append(key)

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    if indices is None:
        if not is_all(selection):
            indices = select(molecular_system, element=element, selection=selection, mask=mask, syntax=syntax)
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

        aux_item, aux_form = where_is_attribute(molecular_system, argument)

        if aux_item is None:
            result = None
        else:
            result = dict_get[aux_form][element][argument](aux_item, **dict_indices)

        attributes.append(result)

    if output_type=='values':
        if len(attributes) == 1:
            return attributes[0]
        else:
            return attributes
    elif output_type=='dictionary':
        return dict(zip(arguments, attributes))

