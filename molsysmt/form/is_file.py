from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def is_file(form, check=True):

    if check:
        from .is_form import is_form
        if not is_form(form):
            raise WrongFormError()

    from molsysmt.api_forms import file_forms

    return (form in file_forms)

