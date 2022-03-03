def merge(item_1, item_2, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import _checking_form
        _checking_form(item_1, check_form=check_form)
        _checking_form(item_2, check_form=check_form)

    raise NotImplementedError

