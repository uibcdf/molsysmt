from .is_openmm_AmberInpcrdFile import is_openmm_AmberInpcrdFile
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        try:
            is_openmm_AmberInpcrdFile(item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

        try:
            is_openmm_AmberInpcrdFile(to_item)
        except:
            raise WrongFormError('openmm.AmberInpcrdFile')

    raise NotImplementedMethodError()

