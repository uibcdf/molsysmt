from .is_string_pdb_id import is_string_pdb_id
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_string_pdb_id(item_1)
        except:
            raise WrongFormError('string:pdb_id')

        try:
            is_string_pdb_id(item_2)
        except:
            raise WrongFormError('string:pdb_id')

    raise NotImplementedMethodError()

