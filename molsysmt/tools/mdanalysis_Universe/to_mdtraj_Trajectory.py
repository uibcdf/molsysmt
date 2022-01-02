def to_mdtraj_Trajectory(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.mdanalysis_Universe import is_mdanalysis_Universe
    from molsysmt.basic import convert

    if not is_mdanalysis_Universe(item):
        raise ValueError

    tmp_item = convert(item, to_form='mdtraj.Trajectory', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

