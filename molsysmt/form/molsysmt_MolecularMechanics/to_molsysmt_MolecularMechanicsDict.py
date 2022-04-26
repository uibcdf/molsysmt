from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_MolecularMechanicsDict(item, check=True):

    if check:

        digest_item(item, 'molsysmt.MolecularMechanics')

    tmp_item = item.to_dict()

    return tmp_item

