from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

def add(to_item, item, check=True):

    if check:

        if not is_mmtf_MMTFDecoder(item):
            raise WrongFormError('mmtf.MMTFDecoder')

        if not is_mmtf_MMTFDecoder(to_item):
            raise WrongFormError('mmtf.MMTFDecoder')


    raise NotImplementedMethodError()

