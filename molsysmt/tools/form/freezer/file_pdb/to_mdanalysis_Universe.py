def to_mdanalysis_Universe(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check=check)

    try:
        from MDAnalysis import Universe
    except:
        from molsysmt._private_tools.exceptions import LibraryNotFound
        raise LibraryNotFound('MDAnalysis')

    from molsysmt.tools.mdanalysis_Universe import extract

    tmp_item = Universe(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

