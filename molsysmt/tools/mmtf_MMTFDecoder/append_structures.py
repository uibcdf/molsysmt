from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

def append_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        if not is_mmtf_MMTFDecoder(item):
            raise WrongFormError('mmtf.MMTFDecoder')

        try:
            step = digest_step

    raise NotImplementedMethodError()

