from molsysmt._private.exceptions import ArgumentError

def digest_output_form(output_form, caller=None):
    """ Checks if the output_form value is supported.

    If the output_form value is a string correctly spelled but not capitalized, the method returns the right name.

    Parameters
    ----------
    output_form: str or list of str
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
        A WrongToFormError is raised if the form name is not supported.

    """
    if output_form is None:
        return None

    from molsysmt.form import is_file
    from molsysmt.form import _dict_forms_lowercase

    if isinstance(output_form, (list, tuple)):
        return [digest_output_form(ii, caller=caller) for ii in output_form]
    else:
        if is_file(output_form):
            return output_form
        else:
            try:
                return _dict_forms_lowercase[output_form.lower()]
            except:
                pass

    raise ArgumentError('output_form', value=output_form, caller=caller, message=None)

