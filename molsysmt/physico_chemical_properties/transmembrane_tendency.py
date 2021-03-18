import numpy as np
from molsysmt._private_tools.exceptions import *

def transmembrane_tendency(molecular_system, selection='all', type='zhao'):

    from molsysmt.multitool import get

    if type == 'zhao':
        from .groups.transmembrane_tendency import zhao as values
    elif type == 'senes':
        from .groups.transmembrane_tendency import senes as values
    else:
        raise NotImplementedError()

    group_types = get(molecular_system, target='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

