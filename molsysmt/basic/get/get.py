from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
from .arguments import where_get_argument
from molsysmt.forms import dict_get

def get(molecular_system, target='atom', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT', **kwargs):

    """get(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='MolSysMT')

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

    from molsysmt.basic import select

    molecular_system = digest_molecular_system(molecular_system)

    # selection works as a mask if indices or ids are used

    target = digest_target(target)
    attributes = [ digest_get_argument(key, target) for key in kwargs.keys() if kwargs[key] ]
    indices = digest_indices(indices)
    frame_indices = digest_frame_indices(frame_indices)

    # doing the work here

    if indices is None:
        if selection is not 'all':
            indices = select(molecular_system, target=target, selection=selection, syntaxis=syntaxis)
        else:
            indices = 'all'

    output = []
    for attribute in attributes:

        result = None

        for where_attribute in where_get_argument[attribute]:
            item = getattr(molecular_system, where_attribute+'_item')
            form = getattr(molecular_system, where_attribute+'_form')
            if item is not None:
                result = dict_get[form][target][attribute](item, indices=indices, frame_indices=frame_indices)
            if result is not None:
                break

        output.append(result)

    output=digest_output(output)
    return output

