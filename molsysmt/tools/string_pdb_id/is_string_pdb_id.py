from molsysmt._private_tools.exceptions import WrongFormError

def is_string_pdb_id(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'builtins.str')

    if output:
        if item.startswith('pdb_id:'):
            output = True
        else:
            from sabueso.tools.string_pdb_id import is_string_pdb_id as sabueso_is_string_pdb_id
            output = sabueso_is_string_pdb_id(item)

    return output

def _checking_form(item, check_form=True):

    if check_form:
        if not is_string_pdb_id(item):
            raise WrongFormError('string:pdb_id')

    pass

