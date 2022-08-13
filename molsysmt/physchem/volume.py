from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
import numpy as np

@digest()
def volume(molecular_system, selection='all', syntax='MolSysMT', definition='grantham'):

    from molsysmt.basic import get

    if definition == 'grantham':
        from .groups.volume import grantham as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, syntax='MolSysMT', name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

