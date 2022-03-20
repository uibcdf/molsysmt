from molsysmt.tools.string_aminoacids3.is_string_aminoacids3 import is_string_aminoacids3
from molsysmt._private_tools.exceptions import WrongFormError
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_string_aminoacids3(item_1)
        except:
            raise WrongFormError('string:aminoacids3')

        try:
            is_string_aminoacids3(item_2)
        except:
            raise WrongFormError('string:aminoacids3')

    raise NotImplementedMethodError()

