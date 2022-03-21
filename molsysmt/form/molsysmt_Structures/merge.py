from .is_molsysmt_Structures import is_molsysmt_Structures
from molsysmt._private.exceptions import WrongFormError
from molsysmt._private.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_molsysmt_Structures(item_1)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            is_molsysmt_Structures(item_2)
        except:
            raise WrongFormError('molsysmt.Structures')

    raise NotImplementedError

