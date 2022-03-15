from molsysmt.tools.string_aminoacids3.is_string_aminoacids3 import is_string_aminoacids3
from molsysmt._private_tools.exceptions import WrongFormError

def add(to_item, item, check=True):

    if check:

        try:
            is_string_aminoacids3(item)
        except:
            raise WrongFormError('string:aminoacids3')

        try:
            is_string_aminoacids3(to_item)
        except:
            raise WrongFormError('string:aminoacids3')

    raise NotImplementedMethodError()
    pass

