from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolSys import is_molsysmt_MolSys

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_molsysmt_MolSys(item_1)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            is_molsysmt_MolSys(item_2)
        except:
            raise WrongFormError('molsysmt.MolSys')


    tmp_item = extract(item_1)
    tmp_item.add(item_2)

    return tmp_item

