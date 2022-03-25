from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_biopython_SeqRecord import is_biopython_SeqRecord

def add(to_item, item, check=True):

    if check:

        try:
            is_biopython_SeqRecord(item)
        except:
            raise WrongFormError('biopython.SeqRecord')

        try:
            is_biopython_SeqRecord(to_item)
        except:
            raise WrongFormError('biopython.SeqRecord')

    raise NotImplementedMethodError()
    pass

