from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_Structures import is_molsysmt_Structures

def add(to_item, item, check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            is_molsysmt_Structures(to_item)
        except:
            raise WrongFormError('molsysmt.Structures')

    to_item.add(item)

    raise NotImplementedError

