from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        try:
            is_file_prmtop(item)
        except:
            raise WrongFormError('file:prmtop')

        try:
            is_file_prmtop(to_item)
        except:
            raise WrongFormError('file:prmtop')

    raise NotImplementedMethodError()

