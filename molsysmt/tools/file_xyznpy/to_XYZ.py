def to_XYZ(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_xyznpy import is_file_xyznpy
    from molsysmt.basic import convert

    if not is_file_xyznpy(item):
        raise ValueError

    tmp_item = convert(item, 'XYZ', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

