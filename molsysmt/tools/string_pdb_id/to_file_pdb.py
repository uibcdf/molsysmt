def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check=check)

    if output_filename is None:
        raise ValueError

    from molsysmt.tools.file_pdb import download, extract

    download_pdb(item, output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename, copy_if_all=False)

    return tmp_item

