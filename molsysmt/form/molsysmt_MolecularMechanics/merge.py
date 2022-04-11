from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        digest_item(item_1, 'molsysmt.MolecularMechanics')
        digest_item(item_2, 'molsysmt.MolecularMechanics')

    raise NotImplementedMethodError()

