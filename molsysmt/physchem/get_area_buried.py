from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_area_buried(molecular_system, selection='all', type='rose'):
    """
    To be written soon...
    """

    from molsysmt.basic import get

    if type == 'rose':
        from .groups.area_buried import rose as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

