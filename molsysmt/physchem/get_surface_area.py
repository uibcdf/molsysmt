from molsysmt._private.argdigest import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
from molsysmt._private.smonitor import NotImplementedMethodError

@arg_digest()
def get_surface_area(molecular_system, element='group', selection='all', syntax='MolSysMT', definition='collantes',
                     skip_digestion=False):
    """
    Getting standard surface area values for elements in a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='group'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    definition : object, default='collantes'
        Argument definition.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list
        List of surface area values in nm^2 for each selected element.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    if definition == 'collantes':
        from .groups.surface_area import collantes as values
    else:
        raise NotImplementedMethodError

    group_types = get(molecular_system, element='group', selection=selection, syntax=syntax, group_name=True)

    output = []

    for ii in group_types:
        output.append(group_table_value(values, ii))

    return output
