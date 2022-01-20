
def to_file_mmtf(item, atom_indices='all', frame_indices='all', output_filename=None, check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check_form=check_form)

    if output_filename is None:
        raise ValueError

    from molsysmt.tools.mmtf_MMTFDecoder import extract
    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False, check_form=False)

    write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)

    tmp_item = output_filename

    return tmp_item

