from ..exceptions import *

syntaxis = [
    'MolSysMT',
    'Amber',
    'MDAnalysis',
    'MDTraj',
    'ParmEd',
    'NGLView',
]

syntaxis_from_lower = { ii.lower():ii for ii in syntaxis }

def digest_syntaxis(syntaxis):

    try:
        syntaxis = syntaxis_from_lower[syntaxis.lower()]
        return syntaxis
    except:
        raise BadCallError()

def digest_to_syntaxis(to_syntaxis):

    if to_syntaxis is None:
        return None
    else:
        return digest_syntaxis(to_syntaxis)

