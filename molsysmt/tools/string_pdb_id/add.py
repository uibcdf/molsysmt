def add(to_item, item, check=True):

    if check:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(to_item, check=check)
        _checking_form(item, check=check)

    raise NotImplementedError


