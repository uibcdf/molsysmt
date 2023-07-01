from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
import numpy as np

@digest()
def get_transmembrane_tendency(molecular_system, selection='all', syntax='MolSysMT', definition='zhao'):

    from molsysmt.basic import get

    if definition == 'zhao':
        from .groups.transmembrane_tendency import zhao as values
    elif definition == 'senes':
        from .groups.transmembrane_tendency import senes as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, syntax=syntax, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

