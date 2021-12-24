def to_molsysmt_Topology(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_mdcrd import is_file_mdcrd
    from molsysmt.basic import convert

    if not is_file_mdcrd(item):
        raise ValueError

    tmp_item = convert(item, 'molsysmt.Topology', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

