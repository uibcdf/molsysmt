from .is_openmm_PDBFile import is_openmm_PDBFile
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_openmm_PDBFile(item_1)
        except:
            raise WrongFormError('openmm.PDBFile')

        try:
            is_openmm_PDBFile(item_2)
        except:
            raise WrongFormError('openmm.PDBFile')

    raise NotImplementedMethodError()

