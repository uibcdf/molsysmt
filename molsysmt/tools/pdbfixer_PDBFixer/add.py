from molsysmt.tools.pdbfixer_PDBFixer.is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private_tools.exceptions import WrongFormError

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

