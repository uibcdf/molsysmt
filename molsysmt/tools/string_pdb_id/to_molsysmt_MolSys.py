def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check=check)

    from molsysmt.tools.string_pdb_id import to_mmtf_MMTFDecoder as string_pdb_id_to_mmtf_MMTFDecoder
    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys
    tmp_item = string_pdb_id_to_mmtf_MMTFDecoder(item, check=False)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

