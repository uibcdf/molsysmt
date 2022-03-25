from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolSys import is_molsysmt_MolSys

def add(to_item, item, check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            is_molsysmt_MolSys(to_item)
        except:
            raise WrongFormError('molsysmt.MolSys')

    to_item.add(item)

    pass

