def to_molsysmt_MolSys(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_inpcrd import is_file_inpcrd
    from molsysmt.basic import convert

    if not is_file_inpcrd(item):
        raise ValueError

    tmp_item = convert(item, 'molsysmt.MolSys', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

