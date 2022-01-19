def add(to_item, item, check_form=True):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(to_item, check_form=check_form)
        _checking_form(item, check_form=check_form)

    raise NotImplementedError


