import numpy as np
from molsysmt._private.exceptions import *

def polarity(molecular_system, selection = 'all', type='grantham'):

    from molsysmt.basic import get

    if type == 'grantham':
        from molsysmt.physico_chemical_properties.groups.polarity import grantham as values
    elif type == 'zimmerman':
        from molsysmt.physico_chemical_properties.groups.polarity import zimmerman as values
    else:
        raise NotImplementedError()

    group_names = get(molecular_system, element='group', selection=selection, group_name=True)

    output = []

    for ii in group_names:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

