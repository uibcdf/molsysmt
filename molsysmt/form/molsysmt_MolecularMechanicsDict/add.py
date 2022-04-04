from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolecularMechanicsDict import is_molsysmt_MolecularMechanicsDict

def add(to_item, item, check=True):

    if check:

        try:
            is_molsysmt_MolecularMechanicsDict(item)
        except:
            raise WrongFormError('molsysmt.MolecularMechanicsDict')

        try:
            is_molsysmt_MolecularMechanicsDict(to_item)
        except:
            raise WrongFormError('molsysmt.MolecularMechanicsDict')

    raise NotImplementedMethodError()
    pass

