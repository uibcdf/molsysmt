from molsysmt.tools.pdbfixer_PDBFixer.is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_mmtf_MMTFDecoder(item_1)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            is_mmtf_MMTFDecoder(item_2)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

    raise NotImplementedMethodError()

