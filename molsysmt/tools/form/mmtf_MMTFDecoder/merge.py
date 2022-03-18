from .is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_mmtf_MMTFDecoder(item_1)
        except:
            raise WrongFormError('mmtf.MMTFDecoder')

        try:
            is_mmtf_MMTFDecoder(item_2)
        except:
            raise WrongFormError('mmtf.MMTFDecoder')

    raise NotImplementedMethodError()

