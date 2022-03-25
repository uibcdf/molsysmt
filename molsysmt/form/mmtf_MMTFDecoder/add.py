from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

def add(to_item, item, check=True):

    if check:

        try:
            is_mmtf_MMTFDecoder(item)
        except:
            raise WrongFormError('mmtf.MMTFDecoder')

        try:
            is_mmtf_MMTFDecoder(to_item)
        except:
            raise WrongFormError('mmtf.MMTFDecoder')

    raise NotImplementedMethodError()
    pass

