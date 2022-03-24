def to_parmed_Structure(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check=check)

    try:
        from parmed import load_file
    except:
        from molsysmt._private.exceptions import LibraryNotFound
        raise LibraryNotFound('parmed')

    from molsysmt.tools.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

