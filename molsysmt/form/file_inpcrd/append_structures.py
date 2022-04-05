from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_file_inpcrd import is_file_inpcrd

def append_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        try:
            is_file_inpcrd(item)
        except:
            raise WrongFormError('file:inpcrd')

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


