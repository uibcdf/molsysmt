# This method must not be digested
def is_file(form):

    from molsysmt.form import _dict_modules, _dict_forms_lowercase
    from molsysmt.basic import get_form

    output = False

    if isinstance(form, str):

        if form.lower() in _dict_forms_lowercase:

            form = _dict_forms_lowercase[form.lower()]
            output = (_dict_modules[form].form_type == 'file')

        else:

            form = get_form(form)
            output = (_dict_modules[form].form_type == 'file')


    return output


