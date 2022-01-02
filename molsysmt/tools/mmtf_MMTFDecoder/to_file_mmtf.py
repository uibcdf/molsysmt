
def to_file_mmtf(item, selection='all', frame_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
    from molsysmt.basic import convert

    if not is_mmtf_MMTFDecoder(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    tmp_item = convert(item, to_form=output_filename, selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

