def to_mdtraj_XTCTrajectoryFile(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_xtc import is_file_xtc
    from molsysmt.basic import convert

    if not is_file_xtc(item):
        raise ValueError

    tmp_item = convert(item, 'mdtraj.XTCTrajectoryFile', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

