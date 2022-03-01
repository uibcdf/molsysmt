def extract(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check_form=check_form)

    if (atom_indices is 'all') and (structure_indices is 'all'):
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

