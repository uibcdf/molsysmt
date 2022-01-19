from molsysmt._private_tools.exceptions import ItemWithWrongForm

def is_molsysmt_Trajectory(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.Trajectory')

    return output

def _checking_form(item, check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    pass

