def add(to_item, item, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(to_item, check=check)
        _checking_form(item, check=check)

    to_item.add(item)

    pass

