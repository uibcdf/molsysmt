from .is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_openmm_AmberPrmtopFile(item_1)
        except:
            raise WrongFormError('openmm.AmberPrmtopFile')

        try:
            is_openmm_AmberPrmtopFile(item_2)
        except:
            raise WrongFormError('openmm.AmberPrmtopFile')

    raise NotImplementedMethodError()

