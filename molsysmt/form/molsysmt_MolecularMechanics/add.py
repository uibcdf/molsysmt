from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolecularMechanics import is_molsysmt_MolecularMechanics

def add(to_item, item, check=True):

    if check:

        try:
            is_molsysmt_MolecularMechanics(item)
        except:
            raise WrongFormError('molsysmt.MolecularMechanics')

        try:
            is_molsysmt_MolecularMechanics(to_item)
        except:
            raise WrongFormError('molsysmt.MolecularMechanics')

    raise NotImplementedMethodError()
    pass

