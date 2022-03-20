from .is_biopython_Seq import is_biopython_Seq
from molsysmt._private.exceptions import WrongFormError

def add(to_item, item, check=True):

    if check:

        try:
            is_biopython_Seq(item)
        except:
            raise WrongFormError('biopython.Seq')

        try:
            is_biopython_Seq(to_item)
        except:
            raise WrongFormError('biopython.Seq')

    raise NotImplementedMethodError()
    pass

