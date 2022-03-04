def merge(item_1, item_2, check=True):

    if check:
        from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import _checking_form
        _checking_form(item_1, check=check)
        _checking_form(item_2, check=check)

    raise NotImplementedError

