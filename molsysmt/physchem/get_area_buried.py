from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest()
def get_area_buried(molecular_system, element='group', selection='all', definition='rose', skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get

    if definition == 'rose':
        from .groups.area_buried import rose as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    output = np.array(output)

    return output

