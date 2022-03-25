from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_biopython_Seq import is_biopython_Seq

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_biopython_Seq(item_1)
        except:
            raise WrongFormError('biopython.Seq')

        try:
            is_biopython_Seq(item_2)
        except:
            raise WrongFormError('biopython.Seq')

    raise NotImplementedMethodError()

