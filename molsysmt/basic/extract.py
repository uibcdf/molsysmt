from molsysmt._private.digestion import digest
from molsysmt._private.lists_and_tuples import is_list_or_tuple
from molsysmt._private.variables import is_all


@digest
def extract(molecular_system, selection='all', structure_indices='all', to_form=None,
        syntax='MolSysMT', copy_if_all=True, check=True):

    """extract(item, selection='all', structure_indices='all', syntax='MolSysMT')

    Extract a subset of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

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

    :func:`molsysmt.select`

    Notes
    -----

    """

    from . import get_form, select, convert
    from molsysmt.api_forms import dict_extract

    if to_form is not None:

        return convert(molecular_system, to_form=to_form, selection=selection, structure_indices=structure_indices,
                       syntax=syntax)

    forms_in = get_form(molecular_system)

    if not is_all(selection):
        atom_indices = select(molecular_system, selection=selection, syntax=syntax, check=False)
    else:
        atom_indices = 'all'

    if not is_list_or_tuple(get_form):
        forms_in = [forms_in]
        molecular_system = [molecular_system]

    output = []

    for form_in, item in zip(forms_in, molecular_system):
        output_item = dict_extract[form_in](item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, check=False)
        output.append(output_item)

    if len(output)==1:
        output=output[0]

    return output

