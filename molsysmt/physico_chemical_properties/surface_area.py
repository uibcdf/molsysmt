import numpy as np
from molsysmt._private_tools.exceptions import *

def surface_area(molecular_system, selection='all', type='collantes'):

    from molsysmt.basic import get

    if type == 'collantes':
        from .groups.surface_area import collantes as values
    else:
        raise NotImplementedError()

    group_types = get(molecular_system, target='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

