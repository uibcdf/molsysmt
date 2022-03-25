from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        try:
            is_mmtf_MMTFDecoder(item)
        except:
            raise WrongFormError('mmtf.MMTFDecoder')

        try:
            step = digest_step(step)
        except:
            raise WrongStepError()

        try:
            time = digest_time(time)
        except:
            raise WrongTimeError()

        try:
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

        try:
            box = digest_box(box)
        except:
            raise WrongBoxError()

    raise NotImplementedError()

    pass

