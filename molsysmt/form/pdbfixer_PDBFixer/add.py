from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            is_pdbfixer_PDBFixer(to_item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

    raise NotImplementedMethodError()
    pass

