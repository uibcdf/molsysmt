from .is_openmm_AmberInpcrdFile import is_openmm_AmberInpcrdFile
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item_1)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            is_openmm_AmberInpcrdFile(item_2)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

    raise NotImplementedMethodError()

