from ..exceptions import *

def digest_selection(selection, syntaxis="MolSysMT"):

    if type(selection) is str:

        from .syntaxis import digest_syntaxis
        syntaxis = digest_syntaxis(syntaxis)

        if syntaxis=='MolSysMT':

            selection=selection.replace('backbone', '(atom_name==["CA", "N", "C", "O"])')

    return selection

