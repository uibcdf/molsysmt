import numpy as np
from molsysmt._private_tools.exceptions import *

def area_buried(molecular_system, selection='all', type='rose'):

    from molsysmt.basic import get

    if type == 'rose':
        from .groups.area_buried import rose as values
    else:
        raise NotImplementedError()

    group_types = get(molecular_system, target='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

