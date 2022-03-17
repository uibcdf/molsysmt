from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_string_pdb_text(item_1)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            is_string_pdb_text(item_2)
        except:
            raise WrongFormError('string:pdb_text')

    raise NotImplementedMethodError()

