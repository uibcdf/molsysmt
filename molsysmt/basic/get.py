from molsysmt._private.exceptions import *
from molsysmt._private.digestion import (digest_element, digest_indices, digest_selection,
                                         digest_syntaxis, digest_structure_indices,
                                         digest_output, digest_argument)
from molsysmt._private.lists_and_tuples import is_list_or_tuple
from molsysmt.attribute.attributes import _required_indices


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
    None
        The method prints out a pandas dataframe with relevant information depending on the element
        chosen.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`

    Notes
    -----

    """
    # TODO: In some cases get doesn't return None. Update docstring with return types.

    from .. import get_form, select, is_molecular_system, where_is_attribute
    from molsysmt.api_forms import dict_get

    if check:

        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeededError()

        element = digest_element(element)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection)
        indices = digest_indices(indices)
        structure_indices = digest_structure_indices(structure_indices)

        arguments = []
        for key in kwargs.keys():
            if kwargs[key]:
                    arguments.append(digest_argument(key, element))

    else:

        arguments = []
        for key in kwargs.keys():
            if kwargs[key]:
                arguments.append(key)

    if not is_list_or_tuple(molecular_system):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    if indices is None:
        if selection is not 'all':
            indices = select(molecular_system, element=element, selection=selection, syntaxis=syntaxis, check=False)
        else:
            indices = 'all'

    output = []

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

        output.append(result)

    output = digest_output(output)

    return output
