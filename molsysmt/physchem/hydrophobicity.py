import numpy as np
from molsysmt._private_tools.exceptions import *

def hydrophobicity(molecular_system, selection='all', type='eisenberg'):

    from molsysmt.basic import get

    if type == 'eisenberg':
        from .groups.hydrophobicity import eisenberg as values
    elif type == 'argos':
        from .groups.hydrophobicity import argos as values
    elif type == 'sweet':
        from .groups.hydrophobicity import sweet as values
    elif type == 'kyte':
        from .groups.hydrophobicity import kyte as values
    elif type == 'abraham':
        from .groups.hydrophobicity import abraham as values
    elif type == 'bull':
        from .groups.hydrophobicity import bull as values
    elif type == 'guy':
        from .groups.hydrophobicity import guy as values
    elif type == 'miyazawa':
        from .groups.hydrophobicity import miyazawa as values
    elif type == 'roseman':
        from .groups.hydrophobicity import roseman as values
    elif type == 'wolfenden':
        from .groups.hydrophobicity import wolfenden as values
    elif type == 'chothia':
        from .groups.hydrophobicity import chothia as values
    elif type == 'hopp':
        from .groups.hydrophobicity import hopp as values
    elif type == 'manavalan':
        from .groups.hydrophobicity import manavalan as values
    elif type == 'black':
        from .groups.hydrophobicity import black as values
    elif type == 'fauchere':
        from .groups.hydrophobicity import fauchere as values
    else:
        raise NotImplementedError()

    group_types = get(molecular_system, target='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

