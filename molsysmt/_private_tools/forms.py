from molsysmt.forms import forms
from molsysmt.tools.items import item_is_file
from molsysmt._private_tools.lists_and_tuples import is_list_or_tuple
from molsysmt._private_tools.exceptions import *

form_from_lowercase = {ii.lower():ii for ii in forms}

def digest_form(form):

    if form_is_file(form):
        output = form
    elif is_list_or_tuple(form):
        output = [digest_form(ii) for ii in form]
    else:
        try:
            output = form_from_lowercase[form.lower()]
        except:
            raise NotImplementedFormError()

    return output

def digest_to_form(to_form):

    if to_form is None:
        return None
    else:
        return digest_form(to_form)

def to_form_is_file(to_form):

    return form_is_file(to_form)

def form_is_file(form):

    output = False

    if type(form) is str:
        if ':' not in form:
            if item_is_file(form):
                output = True

    return output

def form_of_file(to_form):

    output = None

    if form_is_file(to_form):
        output = item_is_file(to_form)

    return output

def are_equal_sets_of_forms(forms1, forms2):

    if not is_list_or_tuple(forms1):
        forms1=[forms1]
    if not is_list_or_tuple(forms2):
        forms2=[forms2]

    output = False
    if set(forms1)==set(forms2):
        output = True

    return output

