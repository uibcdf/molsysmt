def to_molsysmt_Trajectory(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_mmtf import is_file_mmtf
    from molsysmt.basic import convert

    if not is_file_mmtf(item):
        raise ValueError

    tmp_item = convert(item, 'molsysmt.Trajectory', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

