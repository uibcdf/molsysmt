from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt.api_forms import dict_set
from molsysmt.tools.molecular_system import is_molecular_system, where_is_attribute
from molsysmt._private_tools.set_arguments import where_set_argument

def set(molecular_system, target='system', indices=None, selection='all', structure_indices='all', syntaxis='MolSysMT', check=True, **kwargs):

    """into(item, target='system', indices=None, selection='all', structure_indices='all', syntaxis='MolSysMT')

    Set a new value to an attribute.

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

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    structure_indices: int, list, tuple, np.ndarray or 'all', default='all'
        List of indices referring the set of frames this method is going to work with. This set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------

    None
        XXX.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----

    """

    if check:

        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeeded()

        try:
            target = digest_target(target)
        except:
            raise WrongTargetError(target)

        try:
            syntaxis = digest_syntaxis(syntaxis)
        except:
            raise WrongSyntaxisError(syntaxis)

        try:
            selection = digest_selection(selection, syntaxis)
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

        value_of_attribute = {}
        for key in kwargs.keys():
            try:
                value_of_attribute[digest_set_argument(key, target)]=kwargs[key]
            except:
                raise WrongSetArgumentError(key)

    else:

        value_of_attribute = {}
        for key in kwargs.keys():
            value_of_attribute[key]=kwargs[key]


    from molsysmt.basic import select

    # selection works as a mask if indices or ids are used

    attributes = value_of_attribute.keys()

    # doing the work here

    if indices is None:
        if selection is not 'all':
            indices = select(molecular_system, target=target, selection=selection,
                    syntaxis=syntaxis, check=False)
        else:
            indices = 'all'

    for attribute in attributes:

        item, form = where_is_attribute(molecular_system, attribute, check=False)

        value = value_of_attribute[attribute]
        dict_set[form][target][attribute](item, indices=indices, structure_indices=structure_indices, value=value)

    pass

