def to_mdtraj_Topology(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_top import is_file_top
    from molsysmt.basic import convert

    if not is_file_top(item):
        raise ValueError

    tmp_item = convert(item, 'mdtraj.Topology', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

