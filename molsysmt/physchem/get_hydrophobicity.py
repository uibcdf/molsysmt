from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np

def hydrophobicity(molecular_system, selection='all', definition='eisenberg'):

    from molsysmt.basic import get

    if definition == 'eisenberg':
        from .groups.hydrophobicity import eisenberg as values
    elif definition == 'argos':
        from .groups.hydrophobicity import argos as values
    elif definition == 'sweet':
        from .groups.hydrophobicity import sweet as values
    elif definition == 'kyte':
        from .groups.hydrophobicity import kyte as values
    elif definition == 'abraham':
        from .groups.hydrophobicity import abraham as values
    elif definition == 'bull':
        from .groups.hydrophobicity import bull as values
    elif definition == 'guy':
        from .groups.hydrophobicity import guy as values
    elif definition == 'miyazawa':
        from .groups.hydrophobicity import miyazawa as values
    elif definition == 'roseman':
        from .groups.hydrophobicity import roseman as values
    elif definition == 'wolfenden':
        from .groups.hydrophobicity import wolfenden as values
    elif definition == 'chothia':
        from .groups.hydrophobicity import chothia as values
    elif definition == 'hopp':
        from .groups.hydrophobicity import hopp as values
    elif definition == 'manavalan':
        from .groups.hydrophobicity import manavalan as values
    elif definition == 'black':
        from .groups.hydrophobicity import black as values
    elif definition == 'fauchere':
        from .groups.hydrophobicity import fauchere as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

