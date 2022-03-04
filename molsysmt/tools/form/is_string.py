
def is_string(form, check=True):

    if check:
        from molsysmt.tools.form import is_form
        if not is_form(form):
            raise WrongFormError()

    from molsysmt.api_forms import string_forms

    return (form in string_forms)

