from .is_file_inpcrd import is_file_inpcrd
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

        try:
            is_file_inpcrd(to_item)
        except:
            raise WrongFormError('file:inpcrd')

    raise NotImplementedMethodError()
    pass

