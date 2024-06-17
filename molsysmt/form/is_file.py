# This method must not be digested
def is_file(item_or_form):

    from molsysmt.form import _dict_modules, _dict_forms_lowercase
    from molsysmt.basic import get_form
    from pathlib import PosixPath

    output = False

    if isinstance(item_or_form, PosixPath):
        item_or_form = str(item_or_form)

    if isinstance(item_or_form, str):

        if item_or_form.lower() in _dict_forms_lowercase:

            form = item_or_form
            form = _dict_forms_lowercase[form.lower()]
            output = (_dict_modules[form].form_type == 'file')

        else:

            item = item_or_form
            form = get_form(item)
            output = (_dict_modules[form].form_type == 'file')

    return output


