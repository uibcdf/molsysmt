from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolSys import is_molsysmt_MolSys

def merge(item_1, item_2, check=True):

    if check:

        digest_item(item_1, 'molsysmt.MolSys')
        digest_item(item_2, 'molsysmt.MolSys')

    tmp_item = extract(item_1)
    tmp_item.add(item_2)

    return tmp_item

