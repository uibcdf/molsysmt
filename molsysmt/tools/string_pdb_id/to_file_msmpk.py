def to_file_msmpk(item, atom_indices='all', model_indices='all', output_filename=None, check_form=True):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check_form=check_form)

    if output_filename is None:
        raise ValueError

    from molsysmt.tools.string_pdb_id import to_molsysmt_MolSys as string_pdb_id_to_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    tmp_item = string_pdb_id_to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, model_indices=model_indices, check_form=False)
    tmp_item = molsysmt_MolSys_to_file_msmpk(tmp_item, output_filename=output_filename, check_form=False)

    return tmp_item

