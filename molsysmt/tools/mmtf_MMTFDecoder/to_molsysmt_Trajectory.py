def to_molsysmt_Trajectory(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
    from molsysmt.basic import convert

    if not is_mmtf_MMTFDecoder(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.Trajectory', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

