from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private_tools.exceptions import WrongFormError

def add(to_item, item, check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            is_molsysmt_MolSys(to_item)
        except:
            raise WrongFormError('molsysmt.MolSys')

    to_item.add(item)

    pass

