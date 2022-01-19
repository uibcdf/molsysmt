def merge(item_1, item_2, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item_1, check_form=check_form)
        _checking_form(item_2, check_form=check_form)

    tmp_item = extract(item_1)
    tmp_item.add(item_2)

    return tmp_item

