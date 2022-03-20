def to_pytraj_Topology(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.pytraj_Trajectory import is_pytraj_Trajectory
    from molsysmt.basic import convert

    if not is_pytraj_Trajectory(item):
        raise ValueError

    tmp_item = convert(item, to_form='pytraj.Topology', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

