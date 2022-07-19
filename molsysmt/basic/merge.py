from molsysmt._private.exceptions import *
from molsysmt._private.digestion import digest, digest_structure_indices
from molsysmt._private.lists_and_tuples import is_list_or_tuple


@digest
def merge(molecular_systems,
          selections='all',
          structure_indices='all',
          syntax='MolSysMT',
          to_form=None):

    """merge(items=None, selection='all', structure_indices='all', syntax='MolSysMT' to_form=None)

    XXX

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    to_form: str, default='molsysmt.MolSys'
        Any accepted form by MolSysMt for the output object.

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the element
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`
    Notes
    -----

    """

    from . import convert, extract, add

    # if check:
    #
    #     digest_single_molecular_system(molecular_system)
    #     structure_indices = digest_multiple_structure_indices(structure_indices)
    #     syntax = digest_syntax(syntax)
    #     selections = digest_multiple_selections(selections, syntax)
    #     to_form = digest_to_form(to_form)

    n_molecular_systems = len(molecular_systems)

    if not is_list_or_tuple(selections):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not is_list_or_tuple(structure_indices):
        structure_indices = [digest_structure_indices(structure_indices) for ii in range(n_molecular_systems)]
    elif len(structure_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")

    if to_form is None:
        to_molecular_system = extract(molecular_systems[0], selection=selections[0],
                                      structure_indices=structure_indices[0])
    else:
        to_molecular_system = convert(molecular_systems[0], to_form=to_form, selection=selections[0],
                                      structure_indices=structure_indices[0])

    add(to_molecular_system, molecular_systems[1:], selections=selections[1:], structure_indices=structure_indices[1:], check=False)

    return to_molecular_system


