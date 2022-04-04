from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolecularMechanics import is_molsysmt_MolecularMechanics

def to_molsysmt_MolecularMechanicsDict(item, check=True):

    if check:

        try:
            is_molsysmt_MolecularMechanics(item)
        except:
            raise WrongFormError('molsysmt.MolecularMechanics')

    tmp_item = item.to_dict()

    return tmp_item

