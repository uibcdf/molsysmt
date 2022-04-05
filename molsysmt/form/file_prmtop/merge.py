from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_file_prmtop(item_1)
        except:
            raise WrongFormError('file:prmtop')

        try:
            is_file_prmtop(item_2)
        except:
            raise WrongFormError('file:prmtop')

    raise NotImplementedMethodError()

