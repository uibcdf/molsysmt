def to_file_mmtf(item, atom_indices='all', model_indices='all', output_filename=None, check_form=True):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check_form=check_form)

    if output_filename is None:
        raise ValueError

    from molsysmt.tools.file_mmtf import download, extract

    download_pdb(item, output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, model_indices=model_indices, output_filename=output_filename, copy_if_all=False)

    return tmp_item

