from molsysmt.forms import dict_extract
from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.multitool.select import select
from molsysmt.multitool.convert import convert

def extract(molecular_system, selection='all', frame_indices='all', to_form=None, syntaxis='MolSysMT'):

    """extract(item, selection='all', frame_indices='all', syntaxis='MolSysMT')

    Extract a subset of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolSysMT (see: :func:`molsysmt.select`).

    syntaxis: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.select`

    Notes
    -----

    """

    if (selection is 'all') and (frame_indices is 'all') and (to_form is None):
        return copy(molecular_system)

    molecular_system = digest_molecular_system(molecular_system)
    items, forms = molecular_system.get_items()


    frame_indices = digest_frame_indices(frame_indices)
    to_form = digest_to_form(to_form)

    if selection is 'all':
        atom_indices='all'
    else:
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)

    tmp_items = []

    for item, form_in in zip(items, forms):
        form_in = get_form(item)
        if atom_indices is not 'all' or frame_indices is not 'all':
            tmp_item = dict_extract[form_in](item, atom_indices=atom_indices, frame_indices=frame_indices) # si es file debe ir a un temporal para ser renombrado luego
        else:
            tmp_item = copy(item)
        tmp_items.append(tmp_item)

    if to_form is None:
        return tmp_items

    if to_form in forms:
        for aux_item in tmp_items:
            if get_form(aux_item)==to_form:
                return aux_item

    if to_form_is_file(to_form):
        if form_of_file(to_form) in forms:
            for aux_item in tmp_items:
                if get_form(aux_item)==form_of_file(to_form):
                    from os import remove
                    tmp_item = copy(aux_item, output_filename=to_form)
                    for reaux_item in tmp_items:
                        if form_is_file(get_form(reaux_item)):
                            remove(reaux_item)
                    return tmp_item

    tmp_items = convert(tmp_items, to_form=to_form)

    tmp_items = digest_output(tmp_items)

    return tmp_items

