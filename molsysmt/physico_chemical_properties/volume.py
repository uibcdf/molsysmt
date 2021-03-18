import numpy as np
from molsysmt._private_tools.exceptions import *

def volume(molecular_system, selection='all', type='grantham'):

    from molsysmt.multitool import get

    if type == 'grantham':
        from .groups.volume import grantham as values
    else:
        raise NotImplementedError()

    group_types = get(molecular_system, target='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

