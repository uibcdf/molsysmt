def to_mmtf_MMTFDecoder(item, atom_indices='all', model_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check_form=check_form)

    from mmtf import fetch
    from molsysmt.tools.mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder

    tmp_item = item.split(':')[-1]
    tmp_item = fetch(tmp_item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item

