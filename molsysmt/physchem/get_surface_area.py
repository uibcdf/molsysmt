from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
import numpy as np

@digest()
def get_surface_area(molecular_system, element='group', selection='all', syntax='MolSysMT', definition='collantes',
                     skip_digestion=False):
    """
    """

    from molsysmt.basic import get

    if definition == 'collantes':
        from .groups.surface_area import collantes as values
    else:
        raise NotImplementedMethodError

    group_types = get(molecular_system, element='group', selection=selection, syntax=syntax, group_name=True)

    output = []

    for ii in group_types:
        output.append(values[ii.upper()])

    return output

