from ..lists_and_tuples import is_list_or_tuple
from ..exceptions import *


def digest_form(form):

    from molsysmt.api_forms import _dict_forms_lowercase
    from molsysmt.item import is_file

    if is_list_or_tuple(form):
        output = [digest_form(ii) for ii in form]
    else:
        if is_file(form):
            output = form
        else:
            output = _dict_forms_lowercase[form.lower()]

    return output


def digest_to_form(to_form):

    if to_form is None:
        return None
    else:
        return digest_form(to_form)

