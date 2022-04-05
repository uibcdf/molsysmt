from .is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        try:
            is_openmm_AmberPrmtopFile(item)
        except:
            raise WrongFormError('openmm.AmberPrmtopFile')

        try:
            is_openmm_AmberPrmtopFile(to_item)
        except:
            raise WrongFormError('openmm.AmberPrmtopFile')

    raise NotImplementedMethodError()

