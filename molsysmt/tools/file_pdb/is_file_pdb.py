from molsysmt._private_tools.exceptions import WrongFormError

def is_file_pdb(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'builtins.str')

    if output:
        if item.endswith('.pdb'):
            output = True

    return output

def _checking_form(item, check_form=True):

    if check_form:
        if not is_file_pdb(item):
            raise WrongFormError('file:pdb')


