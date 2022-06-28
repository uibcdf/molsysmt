from ..exceptions import WrongSelectionError
from ..lists_and_tuples import is_list_or_tuple


def digest_selection(selection, syntaxis="MolSysMT"):
    """ Checks if a given selection is of the expected type.
    """
    # TODO: this function may not check for all selection types.
    if isinstance(selection, str):
        from .syntaxis import digest_syntaxis
        syntaxis = digest_syntaxis(syntaxis)
        if syntaxis == 'MolSysMT':
            selection = selection.replace('backbone', '(atom_name==["CA", "N", "C", "O"])')
    return selection


def digest_multiple_selections(selections, syntaxis="MolSysMT"):
    if is_list_or_tuple(selections):
        return [digest_selection(ii, syntaxis) for ii in selections]
    else:
        return digest_selection(selections, syntaxis)
