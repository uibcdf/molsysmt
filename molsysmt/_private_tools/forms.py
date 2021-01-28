from molsysmt.forms.classes import list_forms as list_classes_forms
from molsysmt.forms.files import list_forms as list_files_forms
from molsysmt.forms.ids import list_forms as list_ids_forms
from molsysmt.forms.seqs import list_forms as list_seqs_forms
from molsysmt.forms.viewers import list_forms as list_viewers_forms
from .lists_and_tuples import is_list_or_tuple

list_forms = list_classes_forms + list_files_forms + list_ids_forms + list_seqs_forms + list_viewers_forms

_aux = { ii.lower():ii for ii in list_forms}

def digest_form(form):

    if is_list_or_tuple(form):
        output = [digest_form(ii) for ii in form]
    else:
        output = _aux[form.lower()]
    return output

def digest_to_form(to_form):

    if to_form is None:
        return None
    else:
        return digest_form(to_form)

def to_form_is_file(to_form):

    output = False

    if type(to_form) is str:
        if to_form.split('.')[-1] in list_files_forms:
            output = True

    return output

def form_is_file(form):

    output = False

    if type(form) is str:
        if form.split('.')[-1] in list_files_forms:
            output = True

    return output

def formname_of_file(to_form):

    output = None

    if type(to_form)==str:
        if to_form.split('.')[-1] in list_files_forms:
            output = to_form.split('.')[-1]

    return output

