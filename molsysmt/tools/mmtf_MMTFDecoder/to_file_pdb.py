
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
                check_form=True):

    if check_form:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check_form=check_form)

    if output_filename is None:
        raise ValueError

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)
    tmp_item = molsysmt_MolSys_to_file_pdb(tmp_item, output_filename=output_filename, check_form=False)

    return tmp_item

