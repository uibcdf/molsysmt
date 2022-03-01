from molsysmt.api_forms import dict_convert, dict_elements, dict_attributes
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.selection import selection_is_all
from molsysmt._private_tools.forms import to_form_is_file, form_of_file

def convert(molecular_system, to_form='molsysmt.MolSys', selection='all', structure_indices='all', syntaxis='MolSysMT', **kwargs):

    """convert(item, to_form='molsysmt.MolSys', selection='all', structure_indices='all', syntaxis='MolSysMT', **kwargs)

    Convert a molecular model into other form.

    A molecular model in a given accepted form can be converted into any other supported form
    by MolSysMt. The list of supported forms can be found in the section 'XXX'.

    Parameters
    ----------

    item: molecular model
        Molecular model in any supported form by MolSysMT (see: XXX).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    to_form: str, default='molsysmt.MolSys'
        The output object will take the form specified here. This form supported form by MolSysMt
        for the output object.

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------

       item: molecular model

       A new object is returned with the form specified by the argument `to_form`.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.load`, :func:`molsysmt.select`

    Notes
    -----

    """

    from molsysmt.basic import select, get_form

    if to_form is None:
        to_form = get_form(molecular_system)

    molecular_system = digest_molecular_system(molecular_system)
    to_form = digest_to_form(to_form)

    if is_list_or_tuple(to_form):
        tmp_item=[]
        for item_out in to_form:
            tmp_item.append(convert(molecular_system, to_form=item_out, selection=selection, structure_indices=structure_indices, syntaxis=syntaxis))
        return tmp_item

    structure_indices = digest_structure_indices(structure_indices)

    if not selection_is_all(selection):
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
    else:
        atom_indices = 'all'

    conversion_arguments={}

    if to_form_is_file(to_form):
        conversion_arguments['output_filename'] = to_form
        to_form = form_of_file(to_form)

    tmp_item = None

    item = None
    from_form = None

    if is_list_or_tuple(molecular_system):
        raise NotImplementedMethodError()
    else:
        item=molecular_system
        from_form=get_form(molecular_system)

    try:
        tmp_item = dict_convert[from_form][to_form](item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices,
                                                       **conversion_arguments, **kwargs)
    except:
        raise NotImplementedConversionError(from_form, to_form)

    tmp_item = digest_output(tmp_item)

    return tmp_item

