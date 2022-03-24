from .is_string_aminoacids1 import is_string_aminoacids1
from molsysmt._private.exceptions import WrongFormError
from molsysmt._private.exceptions import NotImplementedMethodError

def merge(item_1, item_2, check=True):

    if check:

        try:
            is_string_aminoacids1(item_1)
        except:
            raise WrongFormError('string:aminoacids1')

        try:
            is_string_aminoacids1(item_2)
        except:
            raise WrongFormError('string:aminoacids1')

    raise NotImplementedMethodError()

