from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item_1)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            is_pdbfixer_PDBFixer(item_2)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

    raise NotImplementedMethodError()

