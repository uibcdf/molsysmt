
def digest_selection(selection, syntaxis="MolSysMT"):

    from ..exceptions import WrongSelectionError

    try:

        if type(selection) is str:

            from .syntaxis import digest_syntaxis
            syntaxis = digest_syntaxis(syntaxis)

            if syntaxis=='MolSysMT':

                selection=selection.replace('backbone', '(atom_name==["CA", "N", "C", "O"])')

        return selection

    except:

        raise WrongSelectionError()

def digest_multiple_selections(selections, syntaxis="MolSysMT"):

    from ..lists_and_tuples import is_list_or_tuple

    output = None

    if is_list_or_tuple(selections):

        output = [digest_selection(ii) for ii in selections]

    else:

        output = digest_selection(selections)

    return output

