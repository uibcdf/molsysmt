# This method must not be digested
def is_string(form):

    from molsysmt.form import _dict_modules

    return _dict_modules[form].form_type == 'string'


