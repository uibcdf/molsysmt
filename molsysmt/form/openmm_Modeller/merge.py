from .is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_openmm_Modeller(item_1)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            is_openmm_Modeller(item_2)
        except:
            raise WrongFormError('openmm.Modeller')

    raise NotImplementedMethodError()

