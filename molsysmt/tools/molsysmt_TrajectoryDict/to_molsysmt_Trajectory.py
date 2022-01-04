def to_molsysmt_Trajectory(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.molsysmt_TrajectoryDict import is_molsysmt_TrajectoryDict
    from molsysmt.basic import convert

    if not is_molsysmt_TrajectoryDict(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.Trajectory', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

