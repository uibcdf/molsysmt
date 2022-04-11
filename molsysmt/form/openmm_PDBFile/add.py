from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        digest_item(item, 'pdbfixer.PDBFixer')
        digest_item(to_item, 'pdbfixer.PDBFixer')

    raise NotImplementedMethodError()


