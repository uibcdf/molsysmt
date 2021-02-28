from molsysmt.forms import forms
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple

form_from_lowercase = {ii.lower():ii for ii in forms}

def digest_form(form):

    if form_is_file(form):
        output = form
    elif is_list_or_tuple(form):
        output = [digest_form(ii) for ii in form]
    else:
        output = form_from_lowercase[form.lower()]
    return output

def digest_to_form(to_form):

    if to_form is None:
        return None
    else:
        return digest_form(to_form)

def to_form_is_file(to_form):

    output = False

    if type(to_form) is str:
        if to_form.split('.')[-1] in forms:
            output = True

    return output

def form_is_file(form):

    output = False

    if type(form) is str:
        if form.split('.')[-1] in forms:
            output = True

    return output

def form_of_file(to_form):

    output = None

    if type(to_form)==str:
        if to_form.split('.')[-1] in forms:
            output = to_form.split('.')[-1]

    return output

