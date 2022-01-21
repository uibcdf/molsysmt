def to_parmed_Structure(item, atom_indices='all', model_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check_form=check_form)

    try:
        from parmed import load_file
    except:
        from molsysmt._private_tools.exceptions import LibraryNotFound
        raise LibraryNotFound('parmed')

    from molsysmt.tools.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, frame_indices=model_indices, copy_if_all=False)

    return tmp_item

