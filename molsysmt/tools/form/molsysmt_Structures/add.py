from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import is_molsysmt_Structures
from molsysmt._private_tools.exceptions import WrongFormError

def add(to_item, item, check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            is_molsysmt_Structures(to_item)
        except:
            raise WrongFormError('molsysmt.Structures')

    to_item.add(item)

    raise NotImplementedError

