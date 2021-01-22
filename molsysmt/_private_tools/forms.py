from molsysmt.forms.classes import list_forms as list_classes_forms
from molsysmt.forms.files import list_forms as list_files_forms
from molsysmt.forms.ids import list_forms as list_ids_forms
from molsysmt.forms.seqs import list_forms as list_seqs_forms
from molsysmt.forms.viewers import list_forms as list_viewers_forms

list_forms = list_classes_forms + list_files_forms + list_ids_forms + list_seqs_forms + list_viewers_forms

_aux = { ii.lower():ii for ii in list_forms}

def digest_form(form):

    output = _aux[form.lower()]
    return output

def digest_to_form(to_form):

    if to_form is None:
        return None
    else:
        return digest_form(to_form)

