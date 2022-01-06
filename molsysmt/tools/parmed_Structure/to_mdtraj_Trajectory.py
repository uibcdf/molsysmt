def to_mdtraj_Trajectory(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.parmed_Structure import is_parmed_Structure
    from molsysmt.basic import convert

    if not is_parmed_Structure(item):
        raise ValueError

    tmp_item = convert(item, to_form='mdtraj_Trajectory', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

