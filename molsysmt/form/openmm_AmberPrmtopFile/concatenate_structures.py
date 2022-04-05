from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        try:
            is_openmm_AmberPrmtopFile(item)
        except:
            raise WrongFormError('openmm.AmberPrmtopFile')

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

