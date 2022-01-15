def merge(item_1, item_2, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_MolSys(item_1):
            raise ItemWithWrongForm('molsysmt.MolSys')
        if not is_molsysmt_MolSys(item_2):
            raise ItemWithWrongForm('molsysmt.MolSys')


    tmp_item = extract(item_1)
    tmp_item.add(item_2)

    return tmp_item

