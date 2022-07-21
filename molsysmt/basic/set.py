import numpy as np
from molsysmt._private.digestion import digest


@digest
def set(molecular_system,
        element='system',
        indices=None,
        selection='all',
        structure_indices='all',
        syntax='MolSysMT',
        **kwargs):
    """into(item, element='system', indices=None, selection='all', structure_indices='all', syntax='MolSysMT')

    Set a new value to an attribute.

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
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    structure_indices: int, list, tuple, np.ndarray or 'all', default='all'
        List of indices referring the set of frames this method is going to work with. This set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----

    """

    from . import select, where_is_attribute
    from molsysmt._private.variables import is_all
    from molsysmt.api_forms import dict_set

    value_of_attribute = {}
    for key in kwargs.keys():
        value_of_attribute[key] = kwargs[key]

    # selection works as a mask if indices or ids are used

    attributes = value_of_attribute.keys()

    # doing the work here

    if indices is None:
        if not is_all(selection):
            indices = select(molecular_system,
                             element=element,
                             selection=selection,
                             syntax=syntax)
        else:
            indices = 'all'

    for attribute in attributes:
        item, form = where_is_attribute(molecular_system, attribute)

        value = value_of_attribute[attribute]
        dict_set[form][element][attribute](item, indices=indices, structure_indices=structure_indices, value=value)
