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

            form = _dict_forms_lowercase[item_or_form.lower()]
            output = (_dict_modules[form].form_type == 'file')

        elif item_or_form.startswith('file:'):
            output = True

        else:
            # It might be a file path or a form name with a dot (like openmm.Topology)
            # If it's a file path, get_form will return a form starting with 'file:'
            try:
                form = get_form(item_or_form)
                if form in _dict_modules:
                    output = (_dict_modules[form].form_type == 'file')
            except Exception:
                pass

    return output


