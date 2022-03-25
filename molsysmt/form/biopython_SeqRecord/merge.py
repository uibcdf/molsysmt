from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_biopython_SeqRecord import is_biopython_SeqRecord

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_biopython_SeqRecord(item_1)
        except:
            raise WrongFormError('biopython.SeqRecord')

        try:
            is_biopython_SeqRecord(item_2)
        except:
            raise WrongFormError('biopython.SeqRecord')

    raise NotImplementedMethodError()

