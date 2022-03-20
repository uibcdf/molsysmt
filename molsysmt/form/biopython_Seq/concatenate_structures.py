from .is_biopython_Seq import is_biopython_Seq
from molsysmt._private.exceptions import WrongFormError, WrongStepError
from molsysmt._private.step import digest_step
from molsysmt._private.time import digest_time
from molsysmt._private.coordinates import digest_coordinates
from molsysmt._private.box import digest_box

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        try:
            is_biopython_Seq(item)
        except:
            raise WrongFormError('biopython.Seq')

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

    raise NotImplementedMethodError()

    pass

