from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt.api_forms import dict_get
from .arguments import required_indices, digest_argument

def get(molecular_system, target='system', indices=None, selection='all', structure_indices='all', syntaxis='MolSysMT', **kwargs):

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

    from molsysmt.basic import get_form, select, is_a_molecular_system, where_is_attribute

    if not is_a_molecular_system(molecular_system):
        raise SingleMolecularSystemNeededError()

    if not is_list_or_tuple(molecular_system):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    target = digest_target(target)
    arguments = [ digest_argument(key, target) for key in kwargs.keys() if kwargs[key] ]
    indices = digest_indices(indices)
    structure_indices = digest_structure_indices(structure_indices)

    if indices is None:
        if selection is not 'all':
            indices = select(molecular_system, target=target, selection=selection, syntaxis=syntaxis)
        else:
            indices = 'all'

    output = []

    for argument in arguments:

        dict_indices = {}
        if target != 'system':
            if 'indices' in required_indices[argument]:
                dict_indices['indices']=indices
        if 'structure_indices' in required_indices[argument]:
            dict_indices['structure_indices']=structure_indices

        aux_item, aux_form = where_is_attribute(molecular_system, argument)
        result = dict_get[aux_form][target][argument](aux_item, **dict_indices)
        output.append(result)

    output=digest_output(output)
    return output

