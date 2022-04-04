from .is_molsysmt_MolecularMechanicsDict import is_molsysmt_MolecularMechanicsDict
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_molsysmt_MolecularMechanicsDict(item_1)
        except:
            raise WrongFormError('molsysmt.MolecularMechanicsDict')

        try:
            is_molsysmt_MolecularMechanicsDict(item_2)
        except:
            raise WrongFormError('molsysmt.MolecularMechanicsDict')

    raise NotImplementedMethodError()

