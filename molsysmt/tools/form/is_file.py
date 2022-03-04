
def is_file(form, check=True):

    if check:
        from molsysmt.tools.form import is_form
        if not is_form(form):
            raise WrongFormError()

    from molsysmt.api_forms import file_forms

    return (form in file_forms)

