from molsysmt.tools.string_aminoacids1.is_string_aminoacids1 import is_string_aminoacids1
from molsysmt._private_tools.exceptions import WrongFormError

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

