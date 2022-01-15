def add(to_item, item, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_MolSys(item):
            raise ItemWithWrongForm('molsysmt.MolSys')
        if not is_molsysmt_MolSys(to_item):
            raise ItemWithWrongForm('molsysmt.MolSys')

    to_item.add(item)
    pass

