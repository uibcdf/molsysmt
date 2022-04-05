from .is_file_inpcrd import is_file_inpcrd
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_file_inpcrd(item_1)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            is_file_inpcrd(item_2)
        except:
            raise WrongFormError('file:inpcrd')

    raise NotImplementedMethodError()

