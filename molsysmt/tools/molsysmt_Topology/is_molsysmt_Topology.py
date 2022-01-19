from molsysmt._private_tools.exceptions import ItemWithWrongForm

def is_molsysmt_Topology(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.Topology')

    return output

def _checking_form(item, check_form=True):

    if check_form:
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')

    pass

