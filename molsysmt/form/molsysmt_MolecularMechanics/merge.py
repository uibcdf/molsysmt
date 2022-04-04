from .is_molsysmt_MolecularMechanics import is_molsysmt_MolecularMechanics
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_molsysmt_MolecularMechanics(item_1)
        except:
            raise WrongFormError('molsysmt.MolecularMechanics')

        try:
            is_molsysmt_MolecularMechanics(item_2)
        except:
            raise WrongFormError('molsysmt.MolecularMechanics')

    raise NotImplementedMethodError()

