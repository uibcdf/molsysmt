from molsysmt._private_tools.exceptions import WrongFormError

def is_molsysmt_StructuresCollection(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.structures_collection.StructuresCollection')

    return output

def _checking_form(item, check_form=True):

    if check_form:
        if not is_molsysmt_StructuresCollection(item):
            raise WrongFormError('molsysmt.StructuresCollection')

    pass

