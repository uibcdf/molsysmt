
def to_file_mmtf(item, atom_indices='all', structure_indices='all', output_filename=None):

    if check:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check=check)

    if output_filename is None:
        raise ValueError

    from molsysmt.tools.mmtf_MMTFDecoder import extract
    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)

    tmp_item = output_filename

    return tmp_item

