from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError

def add(to_item, item, check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            is_string_pdb_text(to_item)
        except:
            raise WrongFormError('string:pdb_text')

    raise NotImplementedMethodError()
    pass

