from molsysmt.tools.biopython_SeqRecord.is_biopython_SeqRecord import is_biopython_SeqRecord
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

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

