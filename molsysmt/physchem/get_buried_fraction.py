from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np

def get_buried_fraction(molecular_system, selection='all', definition='janin'):

    from molsysmt.basic import get

    if definition == 'janin':
        from .groups.buried_fraction import janin as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

