from molsysmt._private.exceptions import ArgumentError

methods_where_bool = [
    'molsysmt.basic.compare.compare'
]

def digest_form(form, caller=None):
    """ Checks if the name of the form is supported.

    If the form name is correctly spelled but not capitalized, the method returns the right name.

    Parameters
    ----------
    form: str or list of str
        The name or names of the forms.

    caller: str, optional
        Name of the function or method that is being digested.

    Returns
    -------
     str or list of str
        The name or names of the forms.

    Raises
    ------
    WrongFormError
        A WrongFormError is raised if the form name is not supported.

    """
    from molsysmt.form import is_file
    from molsysmt.api_forms import _dict_forms_lowercase

    if caller in methods_where_bool:

        if isinstance(form, bool):
            return form

    if isinstance(form, (list, tuple)):
        return [digest_form(ii, caller=caller) for ii in form]
    else:
        if is_file(form):
            return form
        else:
            try:
                return _dict_forms_lowercase[form.lower()]
            except:
                pass

    raise ArgumentError('form', value=form, caller=caller, message=None)

