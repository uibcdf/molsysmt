from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        digest_item(item_1, 'string:pdb_id')
        digest_item(item_2, 'string:pdb_id')

    raise NotImplementedMethodError()

