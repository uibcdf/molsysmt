from molsysmt._private.argdigest import arg_digest
from molsysmt.physchem.groups._lookup import group_table_value
from molsysmt._private.smonitor import NotImplementedMethodError

@arg_digest()
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
        output.append(group_table_value(values, ii))

    return output

