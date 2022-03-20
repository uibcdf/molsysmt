from .is_biopython_SeqRecord import is_biopython_SeqRecord
from molsysmt._private.exceptions import WrongFormError

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

