def to_molsysmt_Topology(item, atom_indices='all', model_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.tools.string_pdb_id import to_mmtf_MMTFDecoder as string_pdb_id_to_mmtf_MMTFDecoder
    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology

    tmp_item = string_pdb_id_to_mmtf_MMTFDecoder(item, check_form=False)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, model_indices=model_indices, check_form=False)

    return tmp_item

