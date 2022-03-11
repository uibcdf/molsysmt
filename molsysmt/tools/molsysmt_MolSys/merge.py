from molsysmt.tools.pdbfixer_PDBFixer.is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

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

