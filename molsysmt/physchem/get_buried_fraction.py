from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_buried_fraction(molecular_system, element='group', selection='all', definition='janin', syntax='MolSysMT',
                        skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get

    if definition == 'janin':
        from .groups.buried_fraction import janin as values
    else:
        raise NotImplementedMethodError()

    group_types = get(molecular_system, element='group', selection=selection, group_name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    return output

