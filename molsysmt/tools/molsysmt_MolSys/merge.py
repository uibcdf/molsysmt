def merge(item_1, item_2, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item_1, check=check)
        _checking_form(item_2, check=check)

    tmp_item = extract(item_1)
    tmp_item.add(item_2)

    return tmp_item

