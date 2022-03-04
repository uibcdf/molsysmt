from molsysmt._private_tools.exceptions import WrongFormError

def is_molsysmt_Topology(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.topology.Topology')

    return output

def _checking_form(item, check=True):

    if check:
        if not is_molsysmt_Topology(item):
            raise WrongFormError('molsysmt.Topology')

    pass

