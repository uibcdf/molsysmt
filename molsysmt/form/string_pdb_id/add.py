from .is_string_pdb_id import is_string_pdb_id
from molsysmt._private_tools.exceptions import WrongFormError

def add(to_item, item, check=True):

    if check:

        try:
            is_string_pdb_id(item)
        except:
            raise WrongFormError('string:pdb_id')

        try:
            is_string_pdb_id(to_item)
        except:
            raise WrongFormError('string:pdb_id')

    raise NotImplementedMethodError()
    pass

