import numpy as np
from molsysmt._private_tools.exceptions import *

def buried_fraction(molecular_system, selection='all', type='janin'):

    from molsysmt.basic import get

    if type == 'janin':
        from .groups.buried_fraction import janin as values
    else:
        raise NotImplementedError()

    group_types = get(molecular_system, target='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

