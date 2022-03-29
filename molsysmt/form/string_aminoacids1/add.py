from .is_string_aminoacids1 import is_string_aminoacids1
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add(to_item, item, check=True):

    if check:

        try:
            is_string_aminoacids1(item)
        except:
            raise WrongFormError('string:aminoacids1')

        try:
            is_string_aminoacids1(to_item)
        except:
            raise WrongFormError('string:aminoacids1')

    raise NotImplementedMethodError()
    pass

