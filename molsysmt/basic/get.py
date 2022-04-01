from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.lists_and_tuples import is_list_or_tuple
from molsysmt.attribute.attributes import _required_indices, attribute_synonyms, attributes

def get(molecular_system, target='system', indices=None, selection='all', structure_indices='all',
        syntaxis='MolSysMT', check=True, **kwargs):

    """get(item, target='system', indices=None, selection='all', structure_indices='all', syntaxis='MolSysMT')

    Get specific attributes and observables.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of targetted entities ('atom', 'group' or 'chain') this
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
        The method prints out a pandas dataframe with relevant information depending on the target
        chosen.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`

    Notes
    -----

    """

    from .. import get_form, select, is_molecular_system, where_is_attribute
    from molsysmt.api_forms import dict_get

    if check:

        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeededError()

        try:
            target = digest_target(target)
        except:
            raise WrongTargetError(target)

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection = digest_selection(selection)
        except:
            raise WrongSelectionError(selection)

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

        arguments = []
        for key in kwargs.keys():
            if kwargs[key]:
                try:
                    arguments.append(_digest_argument(key, target))
                except:
                    raise WrongGetArgumentError(key)

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
            indices = select(molecular_system, target=target, selection=selection, syntaxis=syntaxis, check=False)
        else:
            indices = 'all'

    output = []

    for argument in arguments:

        dict_indices = {}
        if target != 'system':
            if 'indices' in _required_indices[argument]:
                dict_indices['indices']=indices
        if 'structure_indices' in _required_indices[argument]:
            dict_indices['structure_indices']=structure_indices

        aux_item, aux_form = where_is_attribute(molecular_system, argument, check=False)
        result = dict_get[aux_form][target][argument](aux_item, **dict_indices)
        output.append(result)

    output=digest_output(output)
    return output

def _digest_argument(argument, target):

    output_argument = argument.lower()
    if output_argument in ['index', 'indices', 'name', 'names', 'id', 'ids', 'type', 'types', 'order']:
        output_argument = ('_').join([target, output_argument])
    if output_argument in attribute_synonyms:
        output_argument = attribute_synonyms[output_argument]
    if output_argument in attributes:
        return output_argument
    else:
        raise WrongGetArgumentError()

